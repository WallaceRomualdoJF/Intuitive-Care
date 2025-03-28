import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

// Configuração robusta do Axios
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 15000,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  transformResponse: [
    function (data) {
      if (typeof data === 'string' && data.trim() === '') {
        throw new Error('Resposta vazia do servidor')
      }
      try {
        return JSON.parse(data)
      } catch (err) {
        throw new Error('Formato de resposta inválido')
      }
    }
  ]
})

// Interceptadores para tratamento global de erros
apiClient.interceptors.request.use(config => {
  config.metadata = { startTime: new Date() }
  return config
})

apiClient.interceptors.response.use(
  response => {
    if (!response.data) {
      throw new Error('Resposta sem dados')
    }
    return response
  },
  error => {
    const errorMessages = {
      'ECONNABORTED': 'Tempo de conexão esgotado',
      'Network Error': 'Erro de rede',
      'Request failed': 'Falha na requisição'
    }
    
    const message = error.response?.data?.detail || 
                   errorMessages[error.message] || 
                   error.message ||
                   'Erro desconhecido'
    
    return Promise.reject(new Error(message))
  }
)

const app = createApp(App)

// Disponibiliza o axios globalmente
app.config.globalProperties.$http = apiClient
app.provide('axios', apiClient)

app.mount('#app')