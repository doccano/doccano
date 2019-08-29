<template>
  <project-list :headers="headers" :projects="projects" :selected="selected" @update="update" />
</template>

<script>
import { mapState } from 'vuex'
import ProjectList from '@/components/organisms/ProjectList'

export default {
  components: {
    ProjectList
  },
  data: () => ({
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
  }),

  computed: {
    ...mapState('ProjectList', ['projects', 'selected'])
  },

  async created() {
    await this.$store.dispatch('ProjectList/getProjectList')
  },

  methods: {
    update(selected) {
      this.$store.commit('ProjectList/updateSelected', selected)
    }
  }
}
</script>
