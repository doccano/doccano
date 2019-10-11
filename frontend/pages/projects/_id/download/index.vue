<template>
  <v-card>
    <v-card-title>
      Export
    </v-card-title>
    <v-card-text>
      <a :href="url" download="docs.json">Download</a>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  layout: 'project',

  computed: {
    url() {
      const projectId = this.$route.params.id
      return `/v1/projects/${projectId}/docs/download`
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
