<template>
  <v-card>
    <v-card-title>
      <h2>Discussão</h2>
    </v-card-title>
    <v-card-text>
      <chat-discussion v-if="currentUserId !== null" :current-user-id="currentUserId" />
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ChatDiscussion from '~/components/discussions/ChatDiscussion.vue'

export default defineComponent({
  name: 'ChatDiscussionPage',
  components: { ChatDiscussion },
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  computed: {
    currentUserId(): number {
      return this.$store.getters['auth/getUserId']
    }
  },

  mounted() {
    this.$store.commit('projects/setPageTitle', 'Discussão de Critérios')
  }
})
</script>
