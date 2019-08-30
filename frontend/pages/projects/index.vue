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
import ProjectList from '@/components/containers/ProjectList'
import ProjectDeletionButton from '@/components/containers/ProjectDeletionButton'
import ProjectCreationButton from '@/components/containers/ProjectCreationButton'

export default {
  layout: 'projects',
  components: {
    ProjectList,
    ProjectCreationButton,
    ProjectDeletionButton
  }
}
</script>
