<template>
  <div>
    <v-btn
      class="mb-2 text-capitalize"
      color="primary"
      @click="dialog=true"
    >
      Add Project
    </v-btn>
    <v-dialog
      v-model="dialog"
      width="800px"
    >
      <form-project-creation @cancel="dialog=false" @create-project="createProject" />
    </v-dialog>
  </div>
</template>

<script>
import FormProjectCreation from '@/components/FormProjectCreation'

export default {
  components: {
    FormProjectCreation
  },
  data: () => ({
    dialog: false
  }),

  methods: {
    createProject(project) {
      this.$store.dispatch('ProjectList/createProject', project)
      this.dialog = false
    }
  }
}
</script>
