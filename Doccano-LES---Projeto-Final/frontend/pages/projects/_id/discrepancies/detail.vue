<template>
  <div>
    <v-alert
      v-if="databaseError"
      type="error"
      dense
      class="mb-4"
    >
      Database unavailable. Please try again later.
    </v-alert>

    <v-card class="chat-card">
      <v-card-title>
        Discrepancy Discussion - {{ datasetName }}
      </v-card-title>
  
      <v-card-text class="chat-body">
        <div v-if="isLoading" class="text-center">
          <v-progress-circular indeterminate></v-progress-circular>
        </div>
        <div v-else-if="error" class="text-center error-message">
          {{ error }}
        </div>
        <v-list v-else dense>
          <template v-if="messages.length > 0">
            <v-list-item
              v-for="(msg, index) in validMessages"
              :key="index"
              :class="{ 'my-message': msg.user === username }"
            >
              <v-list-item-content>
                <v-list-item-title>
                  <strong :style="{ color: getUserColor(msg.user || 'Unknown user') }">{{ msg.user || 'Unknown user' }}:</strong> {{ msg.text || '' }}
                </v-list-item-title>
                <v-list-item-subtitle class="text--secondary">
                  {{ formatDate(msg.created_at) }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
          <div v-else class="text-center pa-4">
            No messages yet. Be the first to comment!
          </div>
        </v-list>
      </v-card-text>
  
      <v-card-actions>
        <v-text-field
          v-model="newMessage"
          dense
          hide-details
          class="flex-grow-1"
          placeholder="Type your message..."
          @keyup.enter="sendMessage"
        />
        <v-btn
          small
          :disabled="!newMessage || isSending"
          @click="sendMessage"
        >
          {{ isSending ? 'Sending...' : 'Send' }}
        </v-btn>
      </v-card-actions>
    </v-card>
    
    <!-- Botão para terminar discussão (visível apenas para admins) -->
    <div v-if="isProjectAdmin && !isDiscussionEnded" class="text-center mt-4">
      <v-btn
        color="primary"
        @click="endDiscussion"
      >
        <v-icon left>
          {{ mdiCheckCircleOutline }}
        </v-icon>
        Terminar Discussão
      </v-btn>
    </div>
    
    <!-- Aviso de discussão terminada -->
    <v-alert
      v-if="isDiscussionEnded"
      type="success"
      outlined
      class="mt-4"
    >
      A discussão foi encerrada. Agora é possível configurar uma votação na seção "Annotation Rules".
      
      <!-- Botão para reverter fechamento (visível apenas para admins) -->
      <div v-if="isProjectAdmin" class="text-center mt-3">
        <v-btn
          color="warning"
          outlined
          small
          @click="reopenDiscussion"
        >
          <v-icon left small>
            {{ mdiRefresh }}
          </v-icon>
          Reverter Fechamento
        </v-btn>
      </div>
    </v-alert>

    <!-- Snackbar para notificações -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
    >
      {{ snackbar.text }}
      <template #action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbar.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>
  
<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import { mdiCheckCircleOutline, mdiRefresh } from '@mdi/js'
import type { DiscrepancyMessage } from '~/domain/models/example/discrepancy'

export default Vue.extend({
  name: 'DiscrepancyDetailPage',
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      messages: [] as Array<DiscrepancyMessage>,
      newMessage: '',
      isLoading: false,
      isSending: false,
      error: null as string | null,
      databaseError: false,
      datasetName: '',
      snackbar: {
        show: false,
        text: '',
        color: 'success',
        timeout: 3000
      },
      isProjectAdmin: false,
      mdiCheckCircleOutline,
      mdiRefresh,
      // Variável local para forçar reatividade
      localDiscussionEnded: false,
      // Paleta de cores para os usuários
      userColors: [
        '#1976D2', // Azul
        '#388E3C', // Verde
        '#F57C00', // Laranja
        '#7B1FA2', // Roxo
        '#D32F2F', // Vermelho
        '#0097A7', // Ciano
        '#455A64', // Azul cinza
        '#E64A19', // Laranja escuro
        '#5D4037', // Marrom
        '#689F38', // Verde claro
        '#303F9F', // Índigo
        '#C2185B', // Rosa
        '#00796B', // Teal
        '#FBC02D', // Amarelo
        '#795548'  // Marrom claro
      ]
    }
  },

  computed: {
    ...mapGetters('auth', ['getUsername']),
    isDiscussionEnded() {
      // Usar variável local para garantir reatividade
      const storeValue = this.$store.getters['discussion/isDiscussionEnded'](this.projectId)
      console.log('isDiscussionEnded computed - projectId:', this.projectId, 'storeValue:', storeValue, 'localValue:', this.localDiscussionEnded)
      return this.localDiscussionEnded
    },
    username(): string {
      return this.getUsername || ''
    },
    projectId(): string {
      return this.$route.params.id
    },
    validMessages() {
      console.log('Processando mensagens válidas:', this.messages)
      const filtered = this.messages.filter(msg => msg.text && msg.text.trim() !== '')
      console.log('Mensagens filtradas:', filtered)
      return filtered
    }
  },

  watch: {
    messages: {
      handler(newMessages) {
        console.log('Mensagens atualizadas:', newMessages)
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      },
      deep: true
    },
    // Sincronizar store com variável local
    '$store.state.discussion.discussionsByProject': {
      handler(newState) {
        console.log('Store discussion mudou:', newState)
        if (this.projectId && newState[this.projectId]) {
          this.localDiscussionEnded = newState[this.projectId].isDiscussionEnded || false
          console.log('Atualizou localDiscussionEnded para:', this.localDiscussionEnded)
        }
      },
      deep: true,
      immediate: true
    }
  },

  created() {
    this.loadMessages()
    this.loadDatasetName()
    this.checkAdminRole()
    // Carregar estado da discussão
    this.$store.dispatch('discussion/initDiscussionState')
    // Inicializar variável local com valor do store
    this.localDiscussionEnded = this.$store.getters['discussion/isDiscussionEnded'](this.projectId)
    console.log('created - localDiscussionEnded inicializado para:', this.localDiscussionEnded)
  },

  methods: {
    formatDate(dt: string) {
      try {
        return new Date(dt).toLocaleString()
      } catch (error) {
        return 'Invalid date'
      }
    },

    // Gera uma cor consistente baseada no nome do usuário
    getUserColor(username: string): string {
      if (!username) return this.userColors[0]
      
      // Função hash simples para gerar um índice baseado no nome
      let hash = 0
      for (let i = 0; i < username.length; i++) {
        const char = username.charCodeAt(i)
        hash = ((hash << 5) - hash) + char
        hash = hash & hash // Converte para 32bit integer
      }
      
      // Garante que o hash seja positivo e dentro do range das cores
      const colorIndex = Math.abs(hash) % this.userColors.length
      const selectedColor = this.userColors[colorIndex]
      
      console.log(`Cor para usuário ${username}: ${selectedColor} (índice: ${colorIndex})`)
      return selectedColor
    },

    // Gera um número de classe CSS baseado no nome do usuário
    getUserColorClass(username: string): number {
      console.log('getUserColorClass chamado para:', username)
      if (!username) return 0
      
      let hash = 0
      for (let i = 0; i < username.length; i++) {
        const char = username.charCodeAt(i)
        hash = ((hash << 5) - hash) + char
        hash = hash & hash
      }
      
      const colorIndex = Math.abs(hash) % this.userColors.length
      console.log(`Usuário ${username} → classe color-${colorIndex}`)
      return colorIndex
    },

    async loadMessages() {
      this.isLoading = true
      this.error = null
      try {
        console.log('Recarregando mensagens...')
        const messages = await this.$repositories.discrepancy.fetchMessages(
          this.projectId
        )
        
        console.log('Resposta da API (tipo):', typeof messages)
        console.log('Resposta da API (valor):', messages)
        
        if (Array.isArray(messages) && messages.length > 0) {
          this.messages = messages.map((msg: Partial<DiscrepancyMessage>) => {
            console.log('Processando mensagem:', msg)
            return {
              id: msg.id || 0,
              user: msg.user || 'Unknown user',
              text: msg.text || '',
              created_at: msg.created_at || new Date().toISOString()
            } as DiscrepancyMessage
          })
          console.log('Mensagens processadas:', this.messages)
          console.log('Número de mensagens:', this.messages.length)
          this.databaseError = false
        } else {
          console.warn('Nenhuma mensagem encontrada ou resposta inválida:', messages)
          this.messages = []
        }
      } catch (error) {
        console.error('Erro ao carregar mensagens:', error)
        if (error.response && error.response.status === 503) {
          this.databaseError = true
          this.error = 'Database unavailable. Please try again later.'
        } else {
          this.error = 'Erro ao carregar mensagens. Por favor, tente novamente.'
        }
        this.messages = []
      } finally {
        this.isLoading = false
      }
    },

    async sendMessage() {
      if (!this.newMessage || this.isSending) return
      
      this.isSending = true
      try {
        const msg = await this.$repositories.discrepancy.postMessage(
          this.projectId,
          this.newMessage
        )
        
        // Garante que a mensagem tenha todas as propriedades necessárias
        if (msg && typeof msg === 'object') {
          const newMsg: DiscrepancyMessage = {
            id: msg.id || 0,
            user: msg.user || this.username,
            text: msg.text || this.newMessage,
            created_at: msg.created_at || new Date().toISOString()
          }
          this.messages.push(newMsg)
        }
        
        this.newMessage = ''
        this.databaseError = false
        this.$nextTick(() => {
          const c = this.$el.querySelector('.chat-body') as HTMLElement
          if (c) c.scrollTop = c.scrollHeight
        })
      } catch (error) {
        console.error('Erro ao enviar mensagem:', error)
        this.databaseError = true
        this.snackbar = {
          show: true,
          text: 'Database unavailable. Please try again later.',
          color: 'error',
          timeout: 5000
        }
      } finally {
        this.isSending = false
      }
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const chatBody = this.$el.querySelector('.chat-body') as HTMLElement
        if (chatBody) {
          chatBody.scrollTop = chatBody.scrollHeight
        }
      })
    },

    async loadDatasetName() {
      try {
        const project = await this.$repositories.project.findById(this.projectId)
        this.datasetName = project.name || 'Dataset without name'
      } catch (error) {
        console.error('Erro ao carregar nome do dataset:', error)
        this.datasetName = 'Error loading name'
      }
    },
    
    async checkAdminRole() {
      try {
        const member = await this.$repositories.member.fetchMyRole(this.projectId)
        this.isProjectAdmin = member.isProjectAdmin
      } catch (error) {
        console.error('Erro ao verificar papel de administrador:', error)
      }
    },
    
    endDiscussion() {
      this.$store.dispatch('discussion/endDiscussion', this.projectId)
      // Atualizar variável local imediatamente
      this.localDiscussionEnded = true
      console.log('endDiscussion - localDiscussionEnded definido para:', this.localDiscussionEnded)
      this.snackbar = {
        show: true,
        text: 'A discussão foi encerrada com sucesso. Agora é possível configurar uma votação na seção "Annotation Rules".',
        color: 'success',
        timeout: 5000
      }
    },
    
    reopenDiscussion() {
      this.$store.dispatch('discussion/reopenDiscussion', this.projectId)
      // Atualizar variável local imediatamente
      this.localDiscussionEnded = false
      console.log('reopenDiscussion - localDiscussionEnded definido para:', this.localDiscussionEnded)
      this.snackbar = {
        show: true,
        text: 'A discussão foi reaberta com sucesso. Agora é possível continuar a discussão.',
        color: 'success',
        timeout: 5000
      }
    }
  }
})
</script>
  
<style scoped>
.chat-card { max-width: 600px; margin: 20px auto; }
.chat-body { max-height: 400px; overflow-y: auto; }
.my-message { background-color: #e0f7fa; }
.error-message { color: red; padding: 20px; }

/* Indicador visual colorido para cada usuário */
.user-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
}

/* Estilos base do nome do usuário */
.username-text {
  font-weight: bold !important;
}

/* Classes de cores específicas */
.username-text.color-0 { color: #1976D2 !important; } /* Azul */
.username-text.color-1 { color: #388E3C !important; } /* Verde */
.username-text.color-2 { color: #F57C00 !important; } /* Laranja */
.username-text.color-3 { color: #7B1FA2 !important; } /* Roxo */
.username-text.color-4 { color: #D32F2F !important; } /* Vermelho */
.username-text.color-5 { color: #0097A7 !important; } /* Ciano */
.username-text.color-6 { color: #455A64 !important; } /* Azul cinza */
.username-text.color-7 { color: #E64A19 !important; } /* Laranja escuro */
.username-text.color-8 { color: #5D4037 !important; } /* Marrom */
.username-text.color-9 { color: #689F38 !important; } /* Verde claro */
.username-text.color-10 { color: #303F9F !important; } /* Índigo */
.username-text.color-11 { color: #C2185B !important; } /* Rosa */
.username-text.color-12 { color: #00796B !important; } /* Teal */
.username-text.color-13 { color: #FBC02D !important; } /* Amarelo */
.username-text.color-14 { color: #795548 !important; } /* Marrom claro */
</style>

<style>
/* CSS global para sobrescrever estilos do Vuetify com maior especificidade */
.v-list-item__title .username-text {
  font-weight: bold !important;
}

.v-list-item__title .username-text.color-0 { color: #1976D2 !important; }
.v-list-item__title .username-text.color-1 { color: #388E3C !important; }
.v-list-item__title .username-text.color-2 { color: #F57C00 !important; }
.v-list-item__title .username-text.color-3 { color: #7B1FA2 !important; }
.v-list-item__title .username-text.color-4 { color: #D32F2F !important; }
.v-list-item__title .username-text.color-5 { color: #0097A7 !important; }
.v-list-item__title .username-text.color-6 { color: #455A64 !important; }
.v-list-item__title .username-text.color-7 { color: #E64A19 !important; }
.v-list-item__title .username-text.color-8 { color: #5D4037 !important; }
.v-list-item__title .username-text.color-9 { color: #689F38 !important; }
.v-list-item__title .username-text.color-10 { color: #303F9F !important; }
.v-list-item__title .username-text.color-11 { color: #C2185B !important; }
.v-list-item__title .username-text.color-12 { color: #00796B !important; }
.v-list-item__title .username-text.color-13 { color: #FBC02D !important; }
.v-list-item__title .username-text.color-14 { color: #795548 !important; }
</style>
  