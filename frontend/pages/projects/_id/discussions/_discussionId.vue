<template>
  <v-container style="padding-top: 100px;">
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <div>
          <h2 v-if="!$fetchState.pending && discussion">💬 {{ discussion.title }}</h2>
          <h2 v-else>💬 Discussion</h2>
          <p v-if="!$fetchState.pending && discussion" class="grey--text text--darken-1 mb-0">
            ⏱ {{ formatDate(discussion.start_date) }} → {{ formatDate(discussion.end_date) }}
          </p>
        </div>

        <v-btn
          text
          color="primary"
          @click="closeChat"
        >
          Back to List
        </v-btn>
      </v-col>

      <v-col cols="12">
        <div v-if="$fetchState.pending" class="text-center pa-12">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
          ></v-progress-circular>
          <p class="mt-4 text--secondary">Loading chat...</p>
        </div>

        <v-alert v-else-if="$fetchState.error" type="error" class="mt-4">
          Could not load the discussion. Please try again.
        </v-alert>

        <div v-else>
          <v-alert
            v-if="isDiscussionClosed && !isProjectAdmin"
            type="info"
            border="left"
            color="grey lighten-3"
            text
            class="mt-4"
          >
            This discussion has been closed and no longer allows messages.
          </v-alert>

          <chat-discussion
            v-if="!isDiscussionClosed || isProjectAdmin"
            :current-user-id="currentUserId"
            :messages="messages"
            :read-only="isDiscussionClosed"
            class="mt-4"
            @send-message="handleSendMessage"
            @retry-message="handleRetryMessage"
          />
        </div>
      </v-col>
    </v-row>

    <v-dialog v-model="showUnsavedDialog" max-width="500" persistent>
      <v-card>
        <v-card-title class="headline">Are you sure you want to leave?</v-card-title>
        <v-card-text class="body-1 pt-4">
          You have unsent messages. If you leave now,
          <strong class="error--text">these messages will be lost</strong>.
          <br><br>
          You can also "Stay on Page" and wait for the connection to be re-established to resend them.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="cancelExit"
          >
            Stay on Page
          </v-btn>
          <v-btn
            color="error"
            text
            @click="confirmExit"
          >
            Leave and Discard
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import ChatDiscussion from '~/components/discussions/ChatDiscussion.vue'

type Message = {
  id: number
  userId: number
  username: string
  text: string
  timestamp: Date
  status?: 'sending' | 'failed'
}

export default defineComponent({
  name: 'DiscussionDetailPage',

  components: {
    ChatDiscussion
  },

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      discussion: null as any,
      messages: [] as Message[],
      isProjectAdmin: false,
      isOnline: true,
      pollingInterval: null as any,
      connectionCheckInterval: null as any,
      showUnsavedDialog: false,
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    projectId(): string {
      return this.$route.params.id
    },
    discussionId(): string {
      return this.$route.params.discussionId
    },
    currentUserId(): number {
      return this.$store.getters['auth/getUserId']
    },
    currentUsername(): string {
      return this.$store.getters['auth/getUsername'] || 'Usuário'
    },
    isDiscussionClosed(): boolean {
      if (!this.discussion) return false
      const todayString = new Date().toISOString().substr(0, 10);
      return this.discussion.end_date <= todayString;
    }
  },

  async fetch() {
    try {
      await Promise.all([
        this.loadDiscussion(),
        this.loadMessages(),
        this.loadAdminStatus()
      ]);
    } catch (e) {
      console.error("Falha ao carregar dados da página de discussão:", e)
    }
  },

  mounted() {
    this.checkConnectionStatus();
    this.connectionCheckInterval = setInterval(this.checkConnectionStatus, 10000);
    this.pollingInterval = setInterval(this.pollForNewMessages, 5000);
    window.addEventListener('beforeunload', this.handleBeforeUnload);
  },

  beforeDestroy() {
    clearInterval(this.connectionCheckInterval);
    clearInterval(this.pollingInterval);
    window.removeEventListener('beforeunload', this.handleBeforeUnload);
  },

  methods: {
    formatDate(dateString: string): string {
      if (!dateString) return '';
      const date = new Date(dateString + 'T00:00:00Z');
      return date.toLocaleDateString('pt-PT', {
        timeZone: 'UTC',
      });
    },

    async loadAdminStatus() {
      const member = await this.$repositories.member.fetchMyRole(this.projectId)
      this.isProjectAdmin = member.isProjectAdmin
    },

    async loadDiscussion() {
      const res = await this.$axios.get(`/v1/projects/${this.projectId}/discussions/${this.discussionId}/`)
      this.discussion = res.data
    },

    async loadMessages() {
      try {
        const res = await this.$axios.get(`/v1/discussions/${this.discussionId}/chat/`)
        this.messages = res.data.map((msg: any) => ({
          id: msg.id,
          userId: msg.userId,
          username: msg.username || 'Usuário',
          text: msg.text,
          timestamp: new Date(msg.timestamp)
        }))
      } catch (e) {
        console.error("Erro ao carregar mensagens:", e);
        this.isOnline = false;
      }
    },
    
    async checkConnectionStatus() {
      try {
        await this.$axios.$head(`/v1/projects/${this.projectId}/discussions/`);
        if (!this.isOnline) {
          console.log('✅ Conexão restabelecida. Pode reenviar as mensagens que falharam.');
          this.isOnline = true;
        }
      } catch (error) {
        if (this.isOnline) {
          console.warn('❌ Conexão perdida.');
          this.isOnline = false;
        }
      }
    },

    async pollForNewMessages() {
      if (!this.isOnline || !this.messages) return;
      try {
        const serverMessages = await this.$axios.$get(`/v1/discussions/${this.discussionId}/chat/`);
        const currentMessageIds = new Set(this.messages.map(m => m.id).filter(id => typeof id === 'number' && id < Date.now()));
        
        const newMessages = serverMessages.filter((msg: Message) => !currentMessageIds.has(msg.id));

        if (newMessages.length > 0) {
          this.messages.push(...newMessages);
        }
      } catch (error) {
        // Silencioso
      }
    },

    async handleSendMessage(text: string) {
      const optimisticMessage: Message = {
        id: Date.now(),
        userId: this.currentUserId,
        username: this.currentUsername,
        text,
        timestamp: new Date(),
        status: 'sending'
      };
      this.messages.push(optimisticMessage);
      if (this.isOnline) {
        try {
          const savedMessage = await this.$axios.$post(`/v1/discussions/${this.discussionId}/chat/`, { text });
          const index = this.messages.findIndex(m => m.id === optimisticMessage.id);
          if (index !== -1) this.$set(this.messages, index, savedMessage);
        } catch (error) {
          this.handleSendFailure(optimisticMessage);
        }
      } else {
        this.handleSendFailure(optimisticMessage);
      }
    },
    
    handleSendFailure(message: Message) {
      const index = this.messages.findIndex(m => m.id === message.id);
      if (index !== -1) {
        this.messages[index].status = 'failed';
        this.queueOfflineMessage(this.messages[index]);
      }
    },

    queueOfflineMessage(message: Message) {
      const queue = JSON.parse(localStorage.getItem(`offline_queue_${this.discussionId}`) || '[]');
      queue.push({ tempId: message.id, text: message.text });
      localStorage.setItem(`offline_queue_${this.discussionId}`, JSON.stringify(queue));
    },

    async handleRetryMessage(messageToRetry: Message) {
      if (!this.isOnline) {
        console.warn("Tentativa de reenvio falhou: sem conexão.");
        return;
      }
      
      const index = this.messages.findIndex(m => m.id === messageToRetry.id);
      if (index === -1) return;

      this.messages[index].status = 'sending';

      try {
        const savedMessage = await this.$axios.$post(
          `/v1/discussions/${this.discussionId}/chat/`, 
          { text: messageToRetry.text }
        );
        this.$set(this.messages, index, savedMessage);
        this.removeMessageFromQueue(messageToRetry.id);
      } catch (error) {
        console.error("O reenvio falhou:", error);
        this.messages[index].status = 'failed';
      }
    },

    removeMessageFromQueue(tempId: number) {
      let queue = JSON.parse(localStorage.getItem(`offline_queue_${this.discussionId}`) || '[]');
      queue = queue.filter((item: any) => item.tempId !== tempId);
      localStorage.setItem(`offline_queue_${this.discussionId}`, JSON.stringify(queue));
    },

    handleBeforeUnload(event: BeforeUnloadEvent) {
      const queue = JSON.parse(localStorage.getItem(`offline_queue_${this.discussionId}`) || '[]');
      if (queue.length > 0) {
        const confirmationMessage = 'As suas mensagens não salvas serão perdidas se sair da página.';
        event.returnValue = confirmationMessage;
        return confirmationMessage;
      }
    },

    closeChat() {
      const queue = JSON.parse(localStorage.getItem(`offline_queue_${this.discussionId}`) || '[]');
      if (queue.length > 0) {
        this.showUnsavedDialog = true;
      } else {
        this.$router.push(`/projects/${this.projectId}/discussions/`);
      }
    },

    cancelExit() {
      this.showUnsavedDialog = false;
    },

    confirmExit() {
      localStorage.removeItem(`offline_queue_${this.discussionId}`);
      this.messages = this.messages.filter(m => m.status !== 'failed');
      this.showUnsavedDialog = false;
      this.$router.push(`/projects/${this.projectId}/discussions/`);
    }
  }
})
</script>

<style scoped>
/* Nenhum estilo extra é necessário aqui */
</style>