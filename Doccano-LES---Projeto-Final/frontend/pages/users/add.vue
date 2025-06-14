<template>
  <div class="user-create-container">
    <!-- Alertas com design melhorado -->
    <v-slide-y-transition>
      <v-alert
        v-if="sucessMessage"
        type="success"
        dismissible
        border="left"
        colored-border
        elevation="2"
        class="ma-4"
        @click="sucessMessage = ''"
      >
        <v-icon slot="prepend" color="success">mdi-check-circle</v-icon>
        {{ sucessMessage }}
      </v-alert>
    </v-slide-y-transition>

    <v-slide-y-transition>
      <v-alert
        v-if="errorMessage"
        type="error"
        dismissible
        border="left"
        colored-border
        elevation="2"
        class="ma-4"
        @click="errorMessage = ''"
      >
        <v-icon slot="prepend" color="error">mdi-alert-circle</v-icon>
        {{ errorMessage }}
      </v-alert>
    </v-slide-y-transition>

    <v-slide-y-transition>
      <v-alert
        v-if="databaseError"
        type="warning"
        dismissible
        border="left"
        colored-border
        elevation="2"
        class="ma-4"
      >
        <v-icon slot="prepend" color="warning">mdi-database-alert</v-icon>
        Base de dados indisponível. Por favor, tente novamente mais tarde.
      </v-alert>
    </v-slide-y-transition>

    <!-- Card principal com design melhorado -->
    <v-card class="main-card" elevation="3">
      <v-card-title class="primary white--text d-flex align-center">
        <v-icon left color="white" size="28">mdi-account-plus</v-icon>
        <span class="text-h5">Criar Novo Utilizador</span>
      </v-card-title>

      <v-card-text class="pa-6">
        <form-create v-bind.sync="editedItem" :items="items">
          <!-- Botões de ação com design melhorado -->
          <div class="actions-container mt-6">
            <div class="d-flex flex-wrap gap-3 justify-center">
              <v-btn
                color="error"
                outlined
                large
                class="action-btn"
                @click="$router.push('/users')"
              >
                <v-icon left>mdi-close</v-icon>
                Cancelar
              </v-btn>

              <v-btn
                :disabled="!isFormValid || databaseError"
                color="primary"
                large
                elevated
                class="action-btn primary-btn"
                @click="save"
              >
                <v-icon left>mdi-content-save</v-icon>
                Guardar
              </v-btn>

              <v-btn
                :disabled="!isFormValid || databaseError"
                color="secondary"
                outlined
                large
                class="action-btn"
                @click="saveAndAnother"
              >
                <v-icon left>mdi-plus</v-icon>
                Guardar e Criar Outro
              </v-btn>
            </div>
          </div>
        </form-create>
      </v-card-text>
    </v-card>

    <!-- Loading overlay -->
    <v-overlay v-if="isLoading" absolute>
      <v-progress-circular
        indeterminate
        size="64"
        color="primary"
      ></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import FormCreate from '~/components/user/FormCreate.vue'
import { UserDTO } from '~/services/application/user/userData'

export default Vue.extend({
  components: {
    FormCreate
  },

  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      editedItem: {
        username: '',
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        passwordConfirmation: '',
        isSuperUser: false,
        isStaff: false
      } as any,
      defaultItem: {
        username: '',
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        passwordConfirmation: '',
        isSuperUser: false,
        isStaff: false
      } as any,
      items: [] as UserDTO[],
      errorMessage: '',
      sucessMessage: '',
      databaseError: false,
      healthCheckInterval: null as any,
      isLoading: false
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    isFormValid(): boolean {
      return !!this.editedItem.username && 
             !!this.editedItem.password && 
             !!this.editedItem.passwordConfirmation && 
             !!this.editedItem.email &&
             this.editedItem.password === this.editedItem.passwordConfirmation;
    },

    service(): any {
      return this.$services.user
    }
  },

  async created() {
    this.isLoading = true
    try {
      this.items = await this.service.list()
    } catch (error) {
      console.error('Error loading users:', error)
      if (error.response && error.response.status === 503) {
        this.databaseError = true
      }
    } finally {
      this.isLoading = false
    }
    
    // Inicia verificação de saúde da base de dados
    this.startHealthCheck()
  },
  
  beforeDestroy() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval)
    }
  },

  methods: {
    async save() {
      this.isLoading = true
      try {
        // Converte para o formato esperado pelo backend
        const userPayload = {
          ...this.editedItem,
          first_name: this.editedItem.firstName,
          last_name: this.editedItem.lastName
        }
        
        await this.service.create(userPayload)
        this.sucessMessage = 'O utilizador foi criado com sucesso!'
        this.databaseError = false
        setTimeout(() => {
          this.$router.push(`/users`)
        }, 1500)
      } catch (error: any) {
        this.handleError(error)
      } finally {
        this.isLoading = false
      }
    },

    async saveAndAnother() {
      this.isLoading = true
      try {
        // Converte para o formato esperado pelo backend
        const userPayload = {
          ...this.editedItem,
          first_name: this.editedItem.firstName,
          last_name: this.editedItem.lastName
        }
        
        await this.service.create(userPayload)
        this.sucessMessage = 'O utilizador foi criado com sucesso! Pode criar outro.'
        this.databaseError = false
        this.editedItem = Object.assign({}, this.defaultItem)
        this.items = await this.service.list()
        
        // Limpa mensagem após 3 segundos
        setTimeout(() => {
          this.sucessMessage = ''
        }, 3000)
      } catch (error) {
        this.handleError(error)
      } finally {
        this.isLoading = false
      }
    },

    handleError(error: any) {
      if (error.response) {
        if (error.response.status === 503) {
          this.databaseError = true
          this.errorMessage = 'Base de dados indisponível. Por favor, tente novamente mais tarde.'
        } else if (error.response.status === 400) {
          const errors = error.response.data
          if (errors.username) {
            this.errorMessage = `Nome de utilizador: ${errors.username[0]}`
          } else if (errors.email) {
            this.errorMessage = `Email: ${errors.email[0]}`
          } else if (errors.password) {
            this.errorMessage = `Palavra-passe: ${errors.password[0]}`
          } else {
            this.errorMessage = 'Dados inválidos. Verifique os campos e tente novamente.'
          }
        } else {
          this.errorMessage = 'Erro ao criar utilizador. Por favor, tente novamente.'
        }
      } else {
        this.databaseError = true
        this.errorMessage = 'Base de dados indisponível. Por favor, tente novamente mais tarde.'
      }
    },
    
    startHealthCheck() {
      // Verifica a saúde da base de dados a cada 2 segundos
      this.healthCheckInterval = setInterval(async () => {
        try {
          await this.$repositories.user.checkHealth()
          this.databaseError = false
        } catch (error) {
          console.error('Database health check failed:', error)
          this.databaseError = true
        }
      }, 2000)
    }
  }
})
</script>

<style scoped>
.user-create-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px;
}

.main-card {
  max-width: 900px;
  margin: 0 auto;
  border-radius: 16px !important;
  overflow: hidden;
}

.v-card-title {
  border-radius: 0 !important;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.v-alert {
  border-radius: 12px !important;
  font-weight: 500;
}

.actions-container {
  padding: 20px;
  background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px;
  margin-top: 20px;
}

.action-btn {
  border-radius: 24px !important;
  text-transform: none !important;
  font-weight: 600;
  padding: 0 24px;
  min-width: 140px;
  margin: 4px;
}

.primary-btn {
  background: linear-gradient(145deg, #1976d2 0%, #1565c0 100%) !important;
}

.gap-3 {
  gap: 12px;
}

/* Transições suaves */
.v-slide-y-transition-enter-active,
.v-slide-y-transition-leave-active {
  transition: all 0.3s ease;
}

.v-slide-y-transition-enter,
.v-slide-y-transition-leave-to {
  transform: translateY(-15px);
  opacity: 0;
}

/* Efeitos de hover nos botões */
.v-btn:hover:not(.v-btn--disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* Animações */
.main-card {
  animation: slideInUp 0.4s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
