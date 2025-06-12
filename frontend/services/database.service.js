import ApiService from './api.service'

class DatabaseService {
  async checkHealth() {
    try {
      console.log('DatabaseService: Calling /database/health endpoint')
      const response = await ApiService.get('/database/health')
      console.log('DatabaseService: Response received:', response.data)
      return {
        isHealthy: response.data.status === 'healthy',
        message: response.data.message,
        status: response.data.status
      }
    } catch (error) {
      console.error('DatabaseService: Error calling health endpoint:', error)
      console.error('DatabaseService: Error response:', error.response)
      return {
        isHealthy: false,
        message: 'Base de dados não disponível, por favor tente mais tarde.',
        status: 'unhealthy'
      }
    }
  }
}

export default new DatabaseService() 