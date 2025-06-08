<template>
  <v-card outlined class="chat-container">
    <v-card-title>
      💬 Chat de Discussão
    </v-card-title>

    <!-- Campo de filtro -->
    <v-text-field
      v-model="filterTerm"
      label="🔍 Filtrar mensagens..."
      prepend-icon="mdi-magnify"
      class="px-4 pb-2"
    />

    <v-card-text class="chat-messages">
      <div v-if="filteredMessages.length === 0" class="text-center pa-4">
        <p>Nenhuma mensagem encontrada.</p>
      </div>
      <div v-else class="message-list">
        <div 
  v-for="(message, index) in filteredMessages" 
  :key="index"
  :class="['message', (message.user || message.userId) === currentUserId ? 'message-own' : 'message-other']"
  :style="(message.user || message.userId) !== currentUserId ? { backgroundColor: getColorForUser(message.userId || message.user) } : {}"
>

          <div class="message-header">
            <strong>{{ message.username }}</strong>
            <small>{{ formatDate(message.timestamp) }}</small>
            <v-btn icon small @click="startReply(message)">
              <v-icon>mdi-reply</v-icon>
            </v-btn>
          </div>
          <div class="message-content">
            <p>{{ message.text }}</p>
          </div>
        </div>
      </div>
    </v-card-text>

    <!-- Mensagem que está sendo respondida -->
    <div v-if="replyTo" class="reply-preview px-4 pb-2">
      <small>Respondendo a: <strong>{{ replyTo.username }}</strong> — {{ replyTo.text }}</small>
      <v-btn icon small @click="cancelReply"><v-icon>mdi-close</v-icon></v-btn>
    </div>

    <v-card-actions>
      <v-textarea
        v-model="newMessage"
        outlined
        rows="3"
        placeholder="Digite sua mensagem..."
        hide-details
        class="chat-input"
        @keydown.enter.prevent="sendMessage"
      />
      <v-btn 
        color="primary" 
        :disabled="!newMessage.trim() || isSending"
        @click="sendMessage"
      >
        Enviar
      </v-btn>
    </v-card-actions>

    <!-- Diálogo de erro -->
    <v-dialog v-model="showError" max-width="500">
      <v-card color="red darken-2" dark>
        <v-card-title class="headline">⚠️ Erro ao enviar mensagem</v-card-title>
        <v-card-text>{{ errorMessage }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="showError = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script lang="ts">


import Vue from 'vue'
import axios from 'axios'

type Message = {
  id: number
  user?: number
  userId?: number
  username: string
  text: string
  timestamp: Date
}

export default Vue.extend({
  name: 'ChatDiscussion',

  props: {
    currentUserId: {
      type: Number,
      required: true,
      default: null
    },
    messages: {
      type: Array as () => Message[],
      default: () => []
    }
  },

  data() {
    return {
      newMessage: '',
      isSending: false,
      localMessages: [] as Message[],
      showError: false,
      errorMessage: '',
      filterTerm: '',
      replyTo: null as Message | null
    }
  },

  computed: {
    filteredMessages(): Message[] {
      // Se temos mensagens como prop, usamos elas, senão usamos as mensagens locais
      const messagesToFilter = this.messages && this.messages.length > 0 ? this.messages : this.localMessages;
      
      if (!this.filterTerm.trim()) return messagesToFilter;

      const term = this.filterTerm.toLowerCase();
      return messagesToFilter.filter((msg) =>
        msg.text.toLowerCase().includes(term) ||
        msg.username.toLowerCase().includes(term)
      );
    }
  },

  watch: {
    messages: {
      handler(newMessages) {
        if (newMessages && newMessages.length > 0) {
          this.$nextTick(() => {
            const container = this.$el.querySelector('.chat-messages');
            if (container) {
              container.scrollTop = container.scrollHeight;
            }
          });
        }
      },
      immediate: true
    }
  },

  mounted() {
    // Se não recebemos mensagens como prop, carregamos do backend
    if ((!this.messages || this.messages.length === 0) && this.$route.params.discussionId) {
      const discussionId = this.$route.params.discussionId;

    axios.get(`/v1/discussions/${discussionId}/chat/`)

        .then((response) => {
          this.localMessages = Array.isArray(response.data)
            ? response.data
            : [];

          this.$nextTick(() => {
            const container = this.$el.querySelector('.chat-messages');
            if (container) {
              container.scrollTop = container.scrollHeight;
            }
          });
        })
        .catch((error) => {
          console.error('Erro ao carregar mensagens:', error);
        });
    }
  },

  methods: {
    formatDate(date: Date): string {
      if (!date) return ''
      const d = new Date(date)
      const dateStr = d.toLocaleDateString('pt-PT', { day: '2-digit', month: '2-digit', year: '2-digit' })
      const timeStr = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      return `${dateStr} ${timeStr}`
    },

    getColorForUser(userId: number): string {
  const colors = ['#FFCDD2', '#F8BBD0', '#E1BEE7', '#BBDEFB', '#C8E6C9', '#FFF9C4', '#FFE0B2', '#D7CCC8'];
  return colors[userId % colors.length];
},

    startReply(message: Message) {
      this.replyTo = message;
    },

    cancelReply() {
      this.replyTo = null;
    },

    async sendMessage() {
      if (!this.newMessage.trim()) return;

      this.isSending = true;
      const messageText = this.replyTo ? 
        `↪ ${this.replyTo.username}: ${this.replyTo.text}\n${this.newMessage}` : 
        this.newMessage;

      try {
        // Se temos mensagens como prop, emitimos o evento para o componente pai
        if (this.messages && this.messages.length > 0) {
          this.$emit('send-message', messageText);
          this.newMessage = '';
          this.replyTo = null;
        } else {
          // Caso contrário, enviamos diretamente para o backend
          const discussionId = this.$route.params.discussionId;
          const response = await axios.post(`/v1/discussions/${discussionId}/chat/`, {
          text: messageText
        });

          const savedMessage = response.data;
          this.localMessages.push(savedMessage);
          this.newMessage = '';
          this.replyTo = null;
        }

        this.$nextTick(() => {
          const container = this.$el.querySelector('.chat-messages');
          if (container) {
            container.scrollTop = container.scrollHeight;
          }
        });

      } catch (error: any) {
        let msg = 'Erro desconhecido.';
        if (!error.response) {
          msg = 'Você não está ligado à base de dados.';
        } else if (error.response.status === 500) {
          msg = 'Você não está ligado à base de dados.';
        } else if (error.response?.data?.detail) {
          msg = error.response.data.detail;
        } else if (error.message) {
          msg = error.message;
        }

        this.errorMessage = msg;
        this.showError = true;
      } finally {
        this.isSending = false;
      }
    }
  }
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 500px;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.chat-messages {
  height: 400px;
  overflow-y: auto;
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 8px;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  padding: 12px 16px;
  border-radius: 16px;
  max-width: 70%;
  font-size: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: background-color 0.3s ease;
}

.message-own {
  align-self: flex-end;
  background-color: #cdeffd;
  color: #003344;
  border-radius: 16px 16px 0 16px;
  margin-left: 40px;
  margin-right: 0;
  text-align: right;
}

.message-other {
  align-self: flex-start;
  background-color: #f1f1f1;
  color: #333;
  border-radius: 16px 16px 16px 0;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

.message-content {
  word-break: break-word;
  font-weight: 400;
}

.chat-input {
  flex-grow: 1;
  margin-right: 10px;
  font-size: 14px;
}

.v-btn {
  border-radius: 20px;
  font-weight: 600;
  text-transform: none;
}

.reply-preview {
  background-color: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 6px 12px;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 8px;
}
</style>