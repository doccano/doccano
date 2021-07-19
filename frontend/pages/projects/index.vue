<template>
  <v-card>
    <v-card-title v-if="isStaff">
      <v-btn
        class="text-capitalize"
        color="primary"
        @click.stop="dialogCreate=true"
      >
        {{ $t('generic.create') }}
      </v-btn>
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete=true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogCreate">
        <form-create
          v-bind.sync="editedItem"
          @cancel="close"
          @save="create"
        />
      </v-dialog>
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          @cancel="dialogDelete=false"
          @remove="remove"
        />
      </v-dialog>
    </v-card-title>
    <project-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
      />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import ProjectList from '@/components/project/ProjectList.vue'
import { ProjectDTO, ProjectWriteDTO } from '~/services/application/project/projectData'
import FormDelete from '~/components/project/FormDelete.vue'
import FormCreate from '~/components/project/FormCreate.vue'

export default Vue.extend({
  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  components: {
    FormCreate,
    FormDelete,
    ProjectList,
  },

  async fetch() {
    this.isLoading = true
    this.items = await this.$services.project.list()
    this.isLoading = false
  },

  data() {
    return {
      dialogCreate: false,
      dialogDelete: false,
      editedItem: {
        name: '',
        description: '',
        projectType: 'DocumentClassification',
        enableRandomOrder: false,
        enableShareAnnotation: false,
        singleClassClassification: false
      } as ProjectWriteDTO,
      defaultItem: {
        name: '',
        description: '',
        projectType: 'DocumentClassification',
        enableRandomOrder: false,
        enableShareAnnotation: false,
        singleClassClassification: false
      } as ProjectWriteDTO,
      items: [] as ProjectDTO[],
      selected: [] as ProjectDTO[],
      isLoading: false
    }
  },

  computed: {
    ...mapGetters('auth', ['isStaff']),
    canDelete(): boolean {
      return this.selected.length > 0
    },
  },

  methods: {
    async create() {
      const project = await this.$services.project.create(this.editedItem)
      this.$router.push(`/projects/${project.id}`)
      this.close()
    },

    close() {
      this.dialogCreate = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
      })
    },
    async remove() {
      await this.$services.project.bulkDelete(this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
