<template>
  <v-card>
    <v-card-title>
      <project-creation-button />
      <project-deletion-button />
    </v-card-title>
    <project-list />
  </v-card>
</template>

<script>
import ProjectList from '@/components/containers/projects/ProjectList'
import ProjectDeletionButton from '@/components/containers/projects/ProjectDeletionButton'
import ProjectCreationButton from '@/components/containers/projects/ProjectCreationButton'

export default {
  layout: 'projects',
  middleware: ['check-auth', 'auth'],
  components: {
    ProjectList,
    ProjectCreationButton,
    ProjectDeletionButton
  }
}
</script>
