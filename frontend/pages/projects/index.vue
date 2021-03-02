<template>
  <v-card>
    <v-card-title>
    </v-card-title>
    <project-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
      />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import ProjectList from '@/components/project/ProjectList.vue'
import { ProjectDTO } from '@/services/application/project.service'

export default Vue.extend({
  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  components: {
    ProjectList,
  },

  async fetch() {
    this.isLoading = true
    this.items = await this.$services.project.list()
    this.isLoading = false
  },

  data() {
    return {
      items: [] as ProjectDTO[],
      selected: [] as ProjectDTO[],
      isLoading: false
    }
  }  
})
</script>
