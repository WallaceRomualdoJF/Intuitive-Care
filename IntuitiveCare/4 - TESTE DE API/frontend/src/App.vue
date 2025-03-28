<template>
  <div id="app" :class="{'api-offline': !apiOnline}">
    <header class="app-header">
      <h1>Sistema de Operadoras de Saúde</h1>
      <div class="api-status" :class="{'online': apiOnline}">
        <i :class="apiOnline ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
        {{ apiOnline ? 'Conectado' : 'Offline' }}
      </div>
    </header>
    
    <main class="app-main">
      <SearchOperadoras v-if="apiOnline" />
      <div v-else class="offline-message">
        <div class="offline-content">
          <i class="fas fa-unlink"></i>
          <h2>Serviço Indisponível</h2>
          <p>Não foi possível conectar ao servidor de dados</p>
          <button @click="checkApiStatus" class="retry-button">
            <i class="fas fa-sync-alt"></i> Tentar Novamente
          </button>
          <p class="last-try" v-if="lastTry">
            Última tentativa: {{ formatTime(lastTry) }}
          </p>
        </div>
      </div>
    </main>
    
    <footer class="app-footer">
      <p>© {{ currentYear }} Intuitive Care - v{{ appVersion }}</p>
      <p v-if="apiOnline && lastUpdate">
        Dados atualizados em: {{ formatDateTime(lastUpdate) }}
      </p>
    </footer>
  </div>
</template>

<script>
import SearchOperadoras from './components/SearchOperadoras.vue'

export default {
  name: 'App',
  components: {
    SearchOperadoras
  },
  data() {
    return {
      apiOnline: false,
      lastUpdate: null,
      lastTry: null,
      currentYear: new Date().getFullYear(),
      appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0'
    }
  },
  async created() {
    await this.checkApiStatus()
    this.interval = setInterval(this.checkApiStatus, 120000) // Verifica a cada 2 minutos
  },
  beforeUnmount() {
    clearInterval(this.interval)
  },
  methods: {
    async checkApiStatus() {
      this.lastTry = new Date()
      try {
        const response = await this.$http.get('/api/info', { timeout: 5000 })
        this.apiOnline = response.data?.status === 'online'
        if (this.apiOnline) {
          this.lastUpdate = new Date()
        }
      } catch (error) {
        this.apiOnline = false
      }
    },
    formatDateTime(date) {
      return date?.toLocaleString('pt-BR') || 'N/A'
    },
    formatTime(date) {
      return date?.toLocaleTimeString('pt-BR') || 'N/A'
    }
  }
}
</script>

<style>
/* Reset e estilos base */
:root {
  --primary-color: #2c3e50;
  --secondary-color: #f5f7fa;
  --success-color: #27ae60;
  --danger-color: #e74c3c;
  --text-color: #333;
  --border-radius: 8px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Roboto', 'Segoe UI', sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background-color: var(--secondary-color);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Layout principal */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

/* Cabeçalho */
.app-header {
  background-color: var(--primary-color);
  color: white;
  padding: 1rem;
  text-align: center;
  position: relative;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.app-header h1 {
  font-size: 1.5rem;
  margin: 0;
  padding: 0 2rem;
}

.api-status {
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.api-status.online {
  background-color: var(--success-color);
}

.api-status:not(.online) {
  background-color: var(--danger-color);
}

/* Conteúdo principal */
.app-main {
  flex: 1;
  padding: 1.5rem;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.offline-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 2rem;
}

.offline-content {
  text-align: center;
  max-width: 400px;
  padding: 2rem;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.offline-content i {
  font-size: 3rem;
  color: var(--danger-color);
  margin-bottom: 1rem;
}

.retry-button {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #1a252f;
}

.last-try {
  margin-top: 1rem;
  font-size: 0.8rem;
  color: #777;
}

/* Rodapé */
.app-footer {
  background-color: #f1f1f1;
  padding: 1rem;
  text-align: center;
  font-size: 0.9rem;
  margin-top: auto;
}

.app-footer p {
  margin: 0.25rem 0;
}

/* Responsividade */
@media (max-width: 768px) {
  .app-header {
    padding: 0.75rem;
  }
  
  .app-header h1 {
    font-size: 1.2rem;
    padding-right: 4rem;
  }
  
  .api-status {
    position: static;
    margin: 0.5rem auto;
    transform: none;
    width: fit-content;
  }
  
  .app-main {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .app-header h1 {
    font-size: 1.1rem;
  }
  
  .offline-content {
    padding: 1.5rem;
  }
  
  .retry-button {
    width: 100%;
    justify-content: center;
  }
}
</style>