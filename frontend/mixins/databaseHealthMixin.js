import DatabaseService from '@/services/database.service'

export const databaseHealthMixin = {
  data() {
    return {
      isDatabaseHealthy: true,
      databaseMessage: '',
      healthCheckInterval: null
    }
  },

  mounted() {
    this.startHealthCheck()
  },

  beforeDestroy() {
    this.stopHealthCheck()
  },

  methods: {
    async checkDatabaseHealth() {
      try {
        const result = await DatabaseService.checkHealth()
        this.isDatabaseHealthy = result.isHealthy
        this.databaseMessage = result.message
      } catch (error) {
        this.isDatabaseHealthy = false
        this.databaseMessage = 'Base de dados não disponível, por favor tente mais tarde.'
      }
    },

    startHealthCheck() {
      // Verificação inicial
      this.checkDatabaseHealth()
      
      // Verificação a cada 10 segundos
      this.healthCheckInterval = setInterval(() => {
        this.checkDatabaseHealth()
      }, 10000)
    },

    stopHealthCheck() {
      if (this.healthCheckInterval) {
        clearInterval(this.healthCheckInterval)
        this.healthCheckInterval = null
      }
    }
  }
} 