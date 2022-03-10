<template>
  <form-create
    v-bind.sync="editedItem"
    @save="create"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import FormCreate from '~/components/project/FormCreate.vue'
import { ProjectWriteDTO } from '~/services/application/project/projectData'

export default Vue.extend({
  components: {
    FormCreate,
  },

  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      editedItem: {
        name: '',
        description: '',
        projectType: 'DocumentClassification',
        enableRandomOrder: false,
        enableShareAnnotation: false,
        singleClassClassification: false,
        allowOverlapping: false,
        graphemeMode: false,
        useRelation: false,
        tags: [] as string[],
      } as ProjectWriteDTO,
      defaultItem: {
        name: '',
        description: '',
        projectType: 'DocumentClassification',
        enableRandomOrder: false,
        enableShareAnnotation: false,
        singleClassClassification: false,
        allowOverlapping: false,
        graphemeMode: false,
        useRelation: false,
        tags: [] as string[],
      } as ProjectWriteDTO,
    }
  },

  methods: {
    async create() {
      const project = await this.$services.project.create(this.editedItem)
      this.$router.push(`/projects/${project.id}`)
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
      })
    },
  }
})
</script>
