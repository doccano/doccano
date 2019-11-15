<template>
  <base-modal
    text="Create"
    :is-create="true"
  >
    <template v-slot="slotProps">
      <project-creation-form
        :create-project="createProject"
        @close="slotProps.close"
      />
    </template>
  </base-modal>
</template>

<script>
import { mapActions } from 'vuex'
import BaseModal from '@/components/molecules/BaseModal'
import ProjectCreationForm from '@/components/organisms/projects/ProjectCreationForm'

export default {
  components: {
    BaseModal,
    ProjectCreationForm
  },

  methods: {
    ...mapActions('projects', ['createProject'])
  }
}
</script>
