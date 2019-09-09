<template>
  <project-list
    :headers="headers"
    :projects="projects"
    :selected="selected"
    :loading="loading"
    @update="update"
  />
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'
import ProjectList from '@/components/organisms/ProjectList'

export default {
  components: {
    ProjectList
  },
  data() {
    return {
      headers: [
        {
          text: 'Name',
          align: 'left',
          value: 'name'
        },
        {
          text: 'Description',
          value: 'description'
        },
        {
          text: 'Type',
          value: 'project_type'
        }
      ]
    }
  },

  computed: {
    ...mapState('projects', ['projects', 'selected', 'loading'])
  },

  created() {
    this.getProjectList()
  },

  methods: {
    ...mapActions('projects', ['getProjectList']),
    ...mapMutations('projects', ['updateSelected']),

    update(selected) {
      this.updateSelected(selected)
    }
  }
}
</script>
