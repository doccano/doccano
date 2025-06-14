<template>
  <form-import :error-message="errorMessage" @clear="clearErrorMessage" @upload="upload" />
</template>

<script lang="ts">
import Vue from 'vue'
import FormImport from '~/components/label/FormImport.vue'

export default Vue.extend({
  components: {
    FormImport
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params, query, store }) {
    if (!['category', 'span', 'relation'].includes(query.type as string)) {
      return false
    }
    if (/^\d+$/.test(params.id)) {
      const project = store.getters['projects/project']
      return project.canDefineLabel
    }
    return false
  },

  data() {
    return {
      errorMessage: ''
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    service(): any {
      const type = this.$route.query.type
      if (type === 'category') {
        return this.$services.categoryType
      } else if (type === 'span') {
        return this.$services.spanType
      } else {
        return this.$services.relationType
      }
    }
  },

  methods: {
    async upload(file: File) {
      try {
        await this.service.upload(this.projectId, file)
        this.$router.push(`/projects/${this.projectId}/labels`)
      } catch (e: any) {
        this.errorMessage = e.message
      }
    },

    clearErrorMessage() {
      this.errorMessage = ''
    }
  }
})
</script>
