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
import ProjectCreationButton from '@/components/organisms/ProjectCreationButton'
import ProjectDeletionButton from '@/components/organisms/ProjectDeletionButton'

export default {
  layout: 'projects',
  components: {
    ProjectList,
    ProjectCreationButton,
    ProjectDeletionButton
  }
}
</script>
