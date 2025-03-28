<template>
  <div class="search-container">
    <div class="search-controls">
      <div class="search-input-group">
        <!-- Search Field -->
        <div class="input-field">
          <i class="fas fa-search icon"></i>
          <input
            type="text"
            v-model="searchTerm"
            placeholder="Digite nome, CNPJ ou registro..."
            @keyup.enter="fetchOperadoras"
            class="search-input"
          />
        </div>

        <!-- Status Select (without dropdown icon) -->
        <select v-model="selectedStatus" class="status-select">
          <option value="Ativa">Ativas</option>
          <option value="Inativa">Inativas</option>
        </select>

        <!-- Search Button -->
        <button @click="fetchOperadoras" class="search-button" :disabled="loading">
          <span v-if="loading" class="loading-spinner"></span>
          {{ loading ? 'Buscando...' : 'Buscar' }}
        </button>
      </div>

      <div class="additional-options">
        <label class="refresh-option">
          <input type="checkbox" v-model="forceRefresh" />
          Forçar atualização
        </label>
        <div v-if="operadoras.length > 0" class="results-count">
          {{ operadoras.length }} resultado{{ operadoras.length !== 1 ? 's' : '' }}
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      <i class="fas fa-exclamation-circle"></i>
      <div class="message-content">
        <p>{{ error }}</p>
      </div>
      <button @click="error = null" class="close-button">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <!-- Results Table -->
    <div v-if="operadoras.length > 0" class="results-section">
      <div class="table-container">
        <table class="operadoras-table">
          <thead>
            <tr>
              <th 
                v-for="field in visibleFields" 
                :key="field"
                @click="sortTable(field)"
                :class="{ 'sortable': true, 'sorted': sortField === field }"
              >
                <div class="header-content">
                  {{ getFieldLabel(field) }}
                  <i 
                    v-if="sortField === field" 
                    :class="sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down'"
                  ></i>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(operadora, index) in sortedOperadoras" :key="index">
              <td v-for="field in visibleFields" :key="`${index}-${field}`">
                {{ formatFieldValue(operadora[field]) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination-controls" v-if="totalPages > 1">
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1"
          class="pagination-button"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="page-indicator">
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        <button 
          @click="currentPage++" 
          :disabled="currentPage === totalPages"
          class="pagination-button"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- No Results Message -->
    <div v-else-if="!loading && searchAttempted" class="no-results">
      <i class="fas fa-search"></i>
      <h3>Nenhum resultado encontrado</h3>
      <p>Modifique seus critérios de busca e tente novamente</p>
    </div>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p>Carregando dados...</p>
      </div>
    </div>

    <!-- Export Button -->
    <button 
      v-if="operadoras.length > 0" 
      @click="exportToCSV" 
      class="export-csv-button"
      :disabled="loading"
    >
      <i class="fas fa-file-csv"></i> Exportar CSV
    </button>
  </div>
</template>

<script>
export default {
  name: 'SearchOperadoras',
  data() {
    return {
      searchTerm: '',
      selectedStatus: 'Ativa',
      forceRefresh: false,
      operadoras: [],
      loading: false,
      error: null,
      searchAttempted: false,
      sortField: null,
      sortDirection: 'asc',
      currentPage: 1,
      itemsPerPage: 15,
      visibleFields: [
        'Razao_Social',
        'Nome_Fantasia',
        'CNPJ',
        'Registro_ANS',
        'Modalidade',
        'UF'
      ],
      fieldLabels: {
        'Razao_Social': 'Razão Social',
        'Nome_Fantasia': 'Nome Fantasia',
        'CNPJ': 'CNPJ',
        'Registro_ANS': 'Registro ANS',
        'Modalidade': 'Modalidade',
        'UF': 'UF'
      }
    }
  },
  computed: {
    sortedOperadoras() {
      let result = [...this.operadoras]
      
      if (this.sortField) {
        result.sort((a, b) => {
          const valA = a[this.sortField] || ''
          const valB = b[this.sortField] || ''
          return this.sortDirection === 'asc' 
            ? valA.localeCompare(valB)
            : valB.localeCompare(valA)
        })
      }
      
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return result.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.operadoras.length / this.itemsPerPage)
    }
  },
  methods: {
    async fetchOperadoras() {
      this.loading = true
      this.error = null
      this.searchAttempted = true
      this.currentPage = 1
      
      try {
        const params = {
          status: this.selectedStatus,
          atualizar: this.forceRefresh
        }
        
        if (this.searchTerm.trim()) {
          params.busca = this.searchTerm.trim()
        }

        const response = await this.$http.get('/api/operadoras', { params })
        
        if (!Array.isArray(response.data)) {
          throw new Error('Formato de dados inválido')
        }
        
        this.operadoras = response.data
      } catch (err) {
        this.error = this.getErrorMessage(err)
        this.operadoras = []
      } finally {
        this.loading = false
      }
    },
    
    async exportToCSV() {
      try {
        this.loading = true
        const response = await this.$http.get('/api/operadoras/export/csv', {
          responseType: 'blob'
        })
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `operadoras_${new Date().toISOString().slice(0,10)}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (err) {
        this.error = this.getErrorMessage(err)
      } finally {
        this.loading = false
      }
    },
    
    sortTable(field) {
      if (this.sortField === field) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortDirection = 'asc'
      }
    },
    
    getFieldLabel(field) {
      return this.fieldLabels[field] || field
    },
    
    formatFieldValue(value) {
      if (value === null || value === undefined) return '-'
      if (typeof value === 'boolean') return value ? 'Sim' : 'Não'
      return value
    },
    
    getErrorMessage(err) {
      const errorMap = {
        'Network Error': 'Erro de conexão com o servidor',
        'timeout': 'Tempo de espera esgotado',
        'Failed to fetch': 'Servidor indisponível'
      }
      
      return errorMap[err.message] || err.message || 'Erro desconhecido'
    }
  }
}
</script>

<style scoped>
.search-container {
  position: relative;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 20px;
}

.search-input-group {
  display: flex;
  gap: 12px;
  margin-bottom: 15px;
  align-items: center;
}

.input-field {
  position: relative;
  flex: 1;
  min-width: 0;
}

.search-input {
  width: 100%;
  padding: 10px 15px 10px 40px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  height: 40px;
  box-sizing: border-box;
}

.status-select {
  width: 50%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  height: 40px;
  background-color: white;
  appearance: none;
}

.search-input-group .icon {
  position: absolute;
  top: 50%;
  left: 15px;
  transform: translateY(-50%);
  color: #7f8c8d;
}

.search-button {
  height: 40px;
  padding: 0 20px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
}

.search-button:hover:not(:disabled) {
  background-color: #1a252f;
}

.search-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.additional-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  margin-bottom: 15px;
}

.error-message {
  background-color: #fadbd8;
  color: #c0392b;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.table-container {
  overflow-x: auto;
  border: 1px solid #ecf0f1;
  border-radius: 4px;
  max-height: 600px;
  overflow-y: auto;
}

.operadoras-table {
  width: 100%;
  border-collapse: collapse;
}

.operadoras-table th {
  background-color: #f8f9fa;
  position: sticky;
  top: 0;
  padding: 12px 15px;
  text-align: left;
  cursor: pointer;
}

.operadoras-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ecf0f1;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.export-csv-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 12px 20px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .search-input-group {
    flex-direction: column;
  }
  
  .search-input,
  .status-select,
  .search-button {
    width: 100%;
  }
  
  .export-csv-button {
    bottom: 20px;
    right: 20px;
    padding: 10px 15px;
  }
}
</style>