<template>
  <v-card outlined class="chat-container">
    <v-card-title>
      💬 Discussion Chat
    </v-card-title>

    <v-text-field
      v-model="filterTerm"
      label="🔍 Filter messages..."
      prepend-icon="mdi-magnify"
      class="px-4 pb-2"
    />

    <v-card-text class="chat-messages" ref="chatMessagesContainer">
      <div v-if="filteredMessages.length === 0" class="text-center pa-4">
        <p>No messages found.</p>
      </div>
      <div v-else class="message-list">
        
        <div 
          v-for="(message, index) in filteredMessages" 
          :key="message.id || index"
          class="message-row"
          :class="{ 'own-row': (message.user || message.userId) === currentUserId }"
        >
          <div
            class="message"
            :class="[(message.user || message.userId) === currentUserId ? 'message-own' : 'message-other']"
            :style="(message.user || message.userId) !== currentUserId ? { backgroundColor: getColorForUser(message.userId || message.user) } : {}"
          >
            <div class="message-header">
              <strong>{{ message.username }}</strong>
              <small>{{ formatDate(message.timestamp) }}</small>
              
              <v-spacer></v-spacer>

              <div v-if="message.status" class="d-flex align-center">
                <v-icon v-if="message.status === 'sending'" small color="grey" title="Sending...">mdi-clock-outline</v-icon>
                
                <div v-if="message.status === 'failed'" class="d-flex align-center">
                  <span class="error--text text--darken-1 mr-2">Failed</span>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        text   
                        x-small
                        color="error"
                        @click="retryMessage(message)"
                        v-bind="attrs"
                        v-on="on"
                        style="min-width: 24px; padding: 0 4px;" 
                      >
                        ⓘ
                      </v-btn>
                    </template>
                    <span>Try again</span>
                  </v-tooltip>
                </div>
              </div>
              
              <v-btn v-else-if="!readOnly" icon small @click="startReply(message)" title="Reply">
                <span style="font-size: 1.5rem; line-height: 1;">⤶</span>
              </v-btn>

            </div>
            <div class="message-content">
              <p>{{ message.text }}</p>
            </div>
          </div>
        </div>

      </div>
    </v-card-text>

    <div v-if="!readOnly">
      <div v-if="replyTo" class="reply-preview px-4 pb-2">
        <small>Replying to: <strong>{{ replyTo.username }}</strong> — {{ replyTo.text }}</small>
        <v-btn icon small @click="cancelReply"><v-icon>mdi-close</v-icon></v-btn>
      </div>

      <v-card-actions>
        <v-textarea
          v-model="newMessage"
          outlined
          rows="3"
          placeholder="Type your message..."
          hide-details
          class="chat-input"
          @keydown.enter.prevent="sendMessage"
        />
        <v-btn 
          color="primary" 
          :disabled="!newMessage.trim()"
          @click="sendMessage"
        >
          Send
        </v-btn>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'

type Message = {
  id: number
  user?: number
  userId?: number
  username: string
  text: string
  timestamp: Date
  status?: 'sending' | 'failed'
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
    },
    readOnly: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      newMessage: '',
      filterTerm: '',
      replyTo: null as Message | null
    }
  },

  computed: {
    filteredMessages(): Message[] {
      if (!this.filterTerm.trim()) return this.messages;

      const term = this.filterTerm.toLowerCase();
      return this.messages.filter((msg) =>
        msg.text.toLowerCase().includes(term) ||
        msg.username.toLowerCase().includes(term)
      );
    }
  },

  watch: {
    messages: {
      handler() {
        this.$nextTick(() => {
          const container = this.$refs.chatMessagesContainer as HTMLElement;
          if (container) {
            container.scrollTop = container.scrollHeight;
          }
        });
      },
      deep: true,
      immediate: true
    }
  },

  methods: {
    formatDate(date: Date): string {
      if (!date) return ''
      const d = new Date(date)
      // Locale alterada para formato de data inglês
      const dateStr = d.toLocaleDateString('en-US', { day: '2-digit', month: '2-digit', year: '2-digit' })
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

    sendMessage() {
      if (!this.newMessage.trim() || this.readOnly) return;

      const messageText = this.replyTo
        ? `↪ ${this.replyTo.username}: ${this.replyTo.text}\n${this.newMessage}`
        : this.newMessage;

      this.$emit('send-message', messageText);

      this.newMessage = '';
      this.replyTo = null;
    },
    
    retryMessage(message: Message) {
      this.$emit('retry-message', message);
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
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}

.chat-messages {
  flex-grow: 1;
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

/* Removido o estilo do ícone fora do balão para corresponder ao pedido */
.message-row {
  display: flex;
  justify-content: flex-start;
}

.message-row.own-row {
  justify-content: flex-end;
}

.message {
  padding: 12px 16px;
  border-radius: 16px;
  max-width: 80%;
  font-size: 15px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.message-own {
  background-color: #cdeffd;
  color: #003344;
  border-radius: 16px 16px 0 16px;
}

.message-other {
  background-color: #f1f1f1;
  color: #333;
  border-radius: 16px 16px 16px 0;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

.message-content {
  word-break: break-word;
  font-weight: 400;
  white-space: pre-wrap;
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