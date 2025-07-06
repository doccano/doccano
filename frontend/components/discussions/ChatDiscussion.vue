<template>
  <div class="modern-chat-container">
    <!-- Header -->
    <div class="chat-header">
      <div class="header-content">
        <div class="chat-title">
          <v-icon color="primary" class="mr-2">mdi-forum</v-icon>
          <h3 class="title-text">Discussion Chat</h3>
        </div>
        <div class="online-indicator">
          <v-chip
            :color="isOnline ? 'success' : 'error'"
            small
            outlined
            class="status-chip"
          >
            <v-icon small left>{{ isOnline ? 'mdi-wifi' : 'mdi-wifi-off' }}</v-icon>
            {{ isOnline ? 'Online' : 'Offline' }}
          </v-chip>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="search-container">
        <v-text-field
          v-model="filterTerm"
          placeholder="Search messages..."
          prepend-inner-icon="mdi-magnify"
          outlined
          dense
          hide-details
          clearable
          class="search-field"
        />
      </div>
    </div>

    <!-- Messages Area -->
    <div ref="messagesContainer" class="messages-container">
      <div v-if="filteredMessages.length === 0" class="empty-state">
        <v-icon size="64" color="grey lighten-1">mdi-message-outline</v-icon>
        <p class="empty-text">{{ filterTerm ? 'No messages found' : 'No messages yet. Start the conversation!' }}</p>
      </div>

      <div v-else class="messages-list">
        <div
          v-for="(message, index) in filteredMessages"
          :key="message.id || index"
          class="message-wrapper"
          :class="{
            'own-message': isOwnMessage(message)
          }"
        >
          <!-- Avatar for other users (always show) -->
          <div v-if="!isOwnMessage(message)" class="message-avatar">
            <v-avatar size="32" :color="getUserColor(message.userId || message.user)">
              <span class="white--text caption font-weight-bold">
                {{ getInitials(message.username) }}
              </span>
            </v-avatar>
          </div>

          <!-- Avatar for own messages (always show) -->
          <div v-if="isOwnMessage(message)" class="message-avatar own-avatar">
            <v-avatar size="32" :color="getUserColor(currentUserId)">
              <span class="white--text caption font-weight-bold">
                {{ getInitials(getCurrentUsername()) }}
              </span>
            </v-avatar>
          </div>

          <!-- Message Bubble -->
          <div class="message-bubble-container">
            <div
              class="message-bubble"
              :class="[
                isOwnMessage(message) ? 'bubble-own' : 'bubble-other',
                getMessageStatus(message)
              ]"
            >
              <!-- Message Header (always show for all messages) -->
              <div class="message-meta">
                <span class="username">{{ message.username }}</span>
                <span class="timestamp">{{ formatTime(message.timestamp) }}</span>
              </div>

              <!-- Reply Reference (if this message is a reply) -->
              <div v-if="message.replyTo" class="reply-reference">
                <div class="reply-bar"></div>
                <div class="reply-content-ref">
                  <span class="reply-author">{{ message.replyTo.username }}</span>
                  <p class="reply-text-ref">{{ truncateText(message.replyTo.text, 80) }}</p>
                </div>
              </div>

              <!-- Message Content -->
              <div class="message-content">
                <p class="message-text">{{ getCleanMessageText(message.text) }}</p>
              </div>

              <!-- Message Footer -->
              <div class="message-footer">
                <!-- Spacer -->
                <div class="flex-grow-1"></div>

                <!-- Retry Button (for failed messages, positioned right) -->
                <v-btn
                  v-if="message.status === 'failed'"
                  text
                  x-small
                  color="error"
                  class="retry-btn"
                  @click="retryMessage(message)"
                >
                  <v-icon size="12" class="mr-1">mdi-refresh</v-icon>
                  Retry
                </v-btn>

                <!-- Reply Button (only for successfully sent messages) -->
                <v-btn
                  v-if="!readOnly && message.status !== 'failed'"
                  text
                  x-small
                  class="reply-btn"
                  @click="replyToMessage(message)"
                >
                  <v-icon size="12">mdi-reply</v-icon>
                  <span class="reply-symbol">↩</span>
                  <span class="reply-text">Reply</span>
                </v-btn>
              </div>

              <!-- Status indicator for own messages -->
              <div v-if="isOwnMessage(message)" class="message-status">
                <v-icon
                  v-if="message.status === 'sending'"
                  size="12"
                  color="grey"
                  class="status-icon"
                >
                  mdi-clock-outline
                </v-icon>
                <v-icon
                  v-else-if="message.status === 'sent'"
                  size="12"
                  color="success"
                  class="status-icon"
                >
                  mdi-check
                </v-icon>
                <v-icon
                  v-else-if="message.status === 'failed'"
                  size="12"
                  color="error"
                  class="status-icon"
                >
                  mdi-alert-circle
                </v-icon>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reply Preview -->
    <div v-if="replyTo && !readOnly" class="reply-preview">
      <div class="reply-content">
        <div class="reply-header">
          <v-icon size="16" color="primary">mdi-reply</v-icon>
          <span class="reply-label">Replying to {{ replyTo.username }}</span>
        </div>
        <p class="reply-text">{{ truncateText(replyTo.text, 100) }}</p>
      </div>
      <v-btn icon small class="reply-close" @click="cancelReply">
        ×
      </v-btn>
    </div>

    <!-- Input Area -->
    <div v-if="!readOnly" class="input-container">
      <div class="input-wrapper">
        <v-textarea
          v-model="newMessage"
          placeholder="Type your message..."
          outlined
          auto-grow
          rows="1"
          max-rows="4"
          hide-details
          class="message-input"
          @keydown.enter.exact.prevent="sendMessage"
          @keydown.shift.enter.prevent="newMessage += '\n'"
        />
        <div class="input-actions">
          <v-btn
            color="primary"
            :disabled="!newMessage.trim()"
            class="send-btn"
            elevation="2"
            @click="sendMessage"
          >
            SEND
          </v-btn>
        </div>
      </div>


    </div>

    <!-- Read-only notice -->
    <div v-else class="readonly-notice">
      <v-icon color="grey" class="mr-2">mdi-lock</v-icon>
      <span class="notice-text">This discussion is read-only</span>
    </div>
  </div>
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
  status?: 'sending' | 'sent' | 'failed'
  replyTo?: {
    id: number
    username: string
    text: string
  }
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
    },
    isOnline: {
      type: Boolean,
      default: true
    },
    currentUsername: {
      type: String,
      default: 'You'
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
          this.scrollToBottom();
        });
      },
      deep: true,
      immediate: true
    }
  },

  methods: {
    isOwnMessage(message: Message): boolean {
      return (message.user || message.userId) === this.currentUserId;
    },

    getInitials(username: string): string {
      if (!username) return '?';
      return username.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },

    getCurrentUsername(): string {
      return this.currentUsername || 'You';
    },

    getUserColor(userId: number): string {
      const colors = [
        '#1976D2', '#388E3C', '#F57C00', '#7B1FA2',
        '#C2185B', '#00796B', '#5D4037', '#455A64'
      ];
      return colors[userId % colors.length];
    },

    getMessageStatus(message: Message): string {
      if (message.status === 'sending') return 'message-sending';
      if (message.status === 'failed') return 'message-failed';
      return '';
    },

    formatTime(date: Date): string {
      if (!date) return '';
      const d = new Date(date);

      // Formato: DD/MM/YYYY HH:MM
      const day = d.getDate().toString().padStart(2, '0');
      const month = (d.getMonth() + 1).toString().padStart(2, '0');
      const year = d.getFullYear();
      const hours = d.getHours().toString().padStart(2, '0');
      const minutes = d.getMinutes().toString().padStart(2, '0');

      return `${day}/${month}/${year} ${hours}:${minutes}`;
    },

    truncateText(text: string, maxLength: number): string {
      if (!text || text.length <= maxLength) return text;
      return text.slice(0, maxLength) + '...';
    },

    getCleanMessageText(text: string): string {
      if (!text) return '';

      // Remove o formato antigo de reply (↪ username: texto\n)
      const replyPattern = /^↪\s+[^:]+:\s+[^\n]*\n/;
      return text.replace(replyPattern, '').trim();
    },

    parseReplyFromText(text: string): { replyTo: any, cleanText: string } | null {
      if (!text || !text.startsWith('↪')) return null;

      const replyPattern = /^↪\s+([^:]+):\s+([^\n]*)\n(.*)$/s;
      const match = text.match(replyPattern);

      if (match) {
        return {
          replyTo: {
            username: match[1].trim(),
            text: match[2].trim()
          },
          cleanText: match[3].trim()
        };
      }

      return null;
    },

    replyToMessage(message: Message) {
      this.replyTo = message;
      this.$nextTick(() => {
        const input = this.$el.querySelector('.message-input textarea') as HTMLTextAreaElement;
        if (input) input.focus();
      });
    },

    cancelReply() {
      this.replyTo = null;
    },

    scrollToBottom() {
      const container = this.$refs.messagesContainer as HTMLElement;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },

    sendMessage() {
      if (!this.newMessage.trim() || this.readOnly) return;

      // Criar objeto de mensagem com reply estruturado
      const messageData = {
        text: this.newMessage,
        replyTo: this.replyTo ? {
          id: this.replyTo.id,
          username: this.replyTo.username,
          text: this.replyTo.text
        } : null
      };

      this.$emit('send-message', messageData);

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
.modern-chat-container {
  display: flex;
  flex-direction: column;
  height: 600px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

/* Header Styles */
.chat-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chat-title {
  display: flex;
  align-items: center;
}

.title-text {
  margin: 0;
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.25rem;
}

.status-chip {
  font-size: 0.75rem !important;
  height: 24px !important;
}

.search-container {
  margin-top: 8px;
}

.search-field {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
}

/* Messages Container */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #95a5a6;
}

.empty-text {
  margin-top: 16px;
  font-size: 1rem;
  text-align: center;
}

/* Messages List */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Message Wrapper */
.message-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  margin-bottom: 4px;
}

/* Avatar */
.message-avatar {
  flex-shrink: 0;
  margin-bottom: 4px;
}

.message-wrapper.own-message {
  flex-direction: row-reverse;
}

/* Message Bubble Container */
.message-bubble-container {
  max-width: 70%;
  min-width: 120px;
}

/* Message Bubble */
.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.bubble-own {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border-bottom-right-radius: 6px;
}

.bubble-other {
  background: white;
  color: #2c3e50;
  border-bottom-left-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.message-sending {
  opacity: 0.7;
  transform: scale(0.98);
}

.message-failed {
  border: 1px solid #e74c3c;
  background: #fdf2f2;
}

.message-failed .message-text {
  color: #2c3e50 !important;
}

.message-failed .username {
  color: #e74c3c !important;
}

.message-failed .timestamp {
  color: #7f8c8d !important;
}

/* Message Meta */
.message-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 0.75rem;
  gap: 8px;
}

.username {
  font-weight: 600;
  color: #667eea;
  flex-shrink: 0;
}

.bubble-own .username {
  color: rgba(255, 255, 255, 0.9);
}

.timestamp {
  color: #95a5a6;
  font-size: 0.65rem;
  white-space: nowrap;
  font-family: 'Courier New', monospace;
  opacity: 0.8;
}

.bubble-own .timestamp {
  color: #2c3e50;
}

/* Reply Reference */
.reply-reference {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
  padding: 8px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.bubble-own .reply-reference {
  background: rgba(255, 255, 255, 0.1);
  border-left-color: rgba(255, 255, 255, 0.5);
}

.reply-bar {
  width: 3px;
  background: #667eea;
  border-radius: 2px;
  min-height: 20px;
}

.bubble-own .reply-bar {
  background: #1976D2;
}

.reply-content-ref {
  flex: 1;
  min-width: 0;
}

.reply-author {
  font-size: 0.7rem;
  font-weight: 600;
  color: #667eea;
  display: block;
  margin-bottom: 2px;
}

.bubble-own .reply-author {
  color: rgba(255, 255, 255, 0.9);
}

.reply-text-ref {
  font-size: 0.75rem;
  color: #7f8c8d;
  margin: 0;
  line-height: 1.3;
  opacity: 0.8;
}

.bubble-own .reply-text-ref {
  color: rgba(255, 255, 255, 0.7);
}

/* Message Content */
.message-content {
  margin-bottom: 8px;
}

.message-text {
  margin: 0;
  line-height: 1.4;
  word-wrap: break-word;
  white-space: pre-wrap;
}

/* Message Footer */
.message-footer {
  display: flex;
  align-items: center;
  margin-top: 6px;
  gap: 8px;
}

.reply-btn, .retry-btn {
  font-size: 0.7rem !important;
  padding: 2px 6px !important;
  min-width: auto !important;
  height: 20px !important;
  background: rgba(0, 0, 0, 0.05) !important;
  color: #667eea !important;
  border-radius: 10px !important;
  text-transform: none !important;
  opacity: 1 !important;
  transition: all 0.2s ease !important;
}

.reply-btn {
  padding: 2px 4px !important;
  width: auto !important;
  overflow: hidden !important;
}

.reply-btn .reply-symbol {
  margin-left: 2px;
  font-size: 0.8rem;
  opacity: 1;
}

.reply-btn .reply-text {
  opacity: 0;
  width: 0;
  margin-left: 0;
  transition: all 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
}

.reply-btn:hover {
  padding: 2px 6px !important;
}

.reply-btn:hover .reply-text {
  opacity: 1;
  width: auto;
  margin-left: 4px;
}

.bubble-own .reply-btn, .bubble-own .retry-btn {
  background: rgba(255, 255, 255, 0.15) !important;
  color: rgba(255, 255, 255, 0.9) !important;
}

.retry-btn {
  color: #e74c3c !important;
}

.bubble-own .retry-btn {
  color: #ffcdd2 !important;
}

.flex-grow-1 {
  flex-grow: 1;
}

.message-status {
  display: flex;
  justify-content: flex-end;
  margin-top: 2px;
}

.status-icon {
  opacity: 0.7;
}

/* Reply Preview */
.reply-preview {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.reply-content {
  flex: 1;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.reply-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #667eea;
}

.reply-text {
  margin: 0;
  font-size: 0.85rem;
  color: #7f8c8d;
  line-height: 1.3;
}

.reply-close {
  background: rgba(231, 76, 60, 0.1) !important;
  color: #e74c3c !important;
  border: 1px solid rgba(231, 76, 60, 0.2) !important;
  transition: all 0.2s ease !important;
  font-size: 16px !important;
  font-weight: bold !important;
  line-height: 1 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.reply-close:hover {
  background: rgba(231, 76, 60, 0.2) !important;
  color: #c0392b !important;
}

/* Input Container */
.input-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.message-input {
  flex: 1;
  background: white;
  border-radius: 20px;
}

.message-input ::v-deep .v-input__control {
  border-radius: 20px;
}

.message-input ::v-deep .v-text-field__details {
  display: none;
}

.input-actions {
  display: flex;
  align-items: center;
}

.send-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
  transition: transform 0.2s ease;
  border-radius: 20px !important;
  padding: 8px 20px !important;
  font-weight: 600 !important;
  text-transform: none !important;
  min-width: auto !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
}

.send-btn:hover {
  transform: scale(1.05);
}

.send-btn:disabled {
  background: #bdc3c7 !important;
  transform: none;
}

/* Connection Warning */
.connection-warning {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 12px;
  padding: 8px 16px;
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 12px;
}

.warning-text {
  font-size: 0.8rem;
  color: #f39c12;
}

/* Read-only Notice */
.readonly-notice {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px 20px;
  background: rgba(149, 165, 166, 0.1);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.notice-text {
  font-size: 0.9rem;
  color: #7f8c8d;
}

/* Responsive Design */
@media (max-width: 768px) {
  .modern-chat-container {
    height: 500px;
    border-radius: 16px;
  }

  .chat-header {
    padding: 16px;
  }

  .messages-container {
    padding: 16px;
  }

  .message-bubble-container {
    max-width: 85%;
  }

  .input-container {
    padding: 16px;
  }

  .title-text {
    font-size: 1.1rem;
  }

  .message-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
  }

  .timestamp {
    font-size: 0.6rem;
  }

  .reply-btn, .retry-btn {
    font-size: 0.65rem !important;
    padding: 1px 3px !important;
    height: 18px !important;
  }

  .reply-btn:hover {
    padding: 1px 4px !important;
  }

  /* Em mobile, mostrar sempre o texto no botão reply */
  .reply-btn .reply-text {
    opacity: 1 !important;
    width: auto !important;
    margin-left: 2px !important;
  }

  .reply-btn .reply-symbol {
    font-size: 0.7rem;
  }
}

@media (max-width: 480px) {
  .message-bubble-container {
    max-width: 90%;
  }

  .message-bubble {
    padding: 10px 14px;
  }

  .input-wrapper {
    gap: 8px;
  }

  .send-btn {
    padding: 6px 12px !important;
    font-size: 0.8rem !important;
  }

  .message-meta {
    gap: 1px;
  }

  .timestamp {
    font-size: 0.55rem;
  }

  .own-timestamp {
    font-size: 0.55rem;
  }
}

/* Animation for new messages */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-wrapper {
  animation: slideInUp 0.3s ease-out;
}

/* Hover effects */
.message-bubble:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.bubble-own:hover {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}
</style>