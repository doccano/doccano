<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h2>💬 {{ discussion?.title || 'Discussão' }}</h2>
        <p v-if="discussion">⏱ {{ formatDate(discussion.start_date) }} → {{ formatDate(discussion.end_date) }}</p>
      </v-col>

      <v-col cols="12">
        <v-alert
          v-if="isDiscussionClosed"
          type="info"
          border="left"
          color="grey lighten-3"
          text
        >
          Esta discussão foi encerrada e não permite mais mensagens.
        </v-alert>

        <chat-discussion
          v-else
          :current-user-id="currentUserId"
          :messages="messages"
          @send-message="handleSendMessage"
        />
      </v-col>
    </v-row>
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
      messages: [] as Message[]
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
      const now = new Date()
      return new Date(this.discussion.end_date) < now
    }
  },

  async fetch() {
    await this.loadDiscussion()
    await this.loadMessages()
  },

  methods: {
    formatDate(date: string): string {
      return new Date(date).toLocaleDateString('pt-PT')
    },

    async loadDiscussion() {
      try {
        const res = await this.$axios.get(`/projects/${this.projectId}/discussions/${this.discussionId}`)
        this.discussion = res.data
      } catch (err) {
        console.error('Erro ao carregar discussão:', err)
      }
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
      } catch (err) {
        console.error('Erro ao carregar mensagens:', err)
      }
    },

    async handleSendMessage(text: string) {
      try {
        const res = await this.$axios.post(
          `/v1/discussions/${this.discussionId}/chat/`,
          {
            text
          }
        )

        const newMsg: Message = {
          id: res.data.id,
          userId: this.currentUserId,
          username: this.currentUsername,
          text,
          timestamp: new Date(res.data.timestamp || Date.now())
        }

        this.messages.push(newMsg)
      } catch (err) {
        console.error('Erro ao enviar mensagem:', err)
      }
    }
  }
})
</script>
