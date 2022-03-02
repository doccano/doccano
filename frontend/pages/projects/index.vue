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
      :items="projects.items"
      :is-loading="isLoading"
      :total="projects.count"
      @update:query="updateQuery"
    />
  </v-card>
</template>

<script lang="ts">
import _ from 'lodash'
import Vue from 'vue'
import { mapGetters } from 'vuex'
import ProjectList from '@/components/project/ProjectList.vue'
import { ProjectDTO, ProjectWriteDTO, ProjectListDTO } from '~/services/application/project/projectData'
import FormDelete from '~/components/project/FormDelete.vue'
import FormCreate from '~/components/project/FormCreate.vue'

export default Vue.extend({

  components: {
    FormCreate,
    FormDelete,
    ProjectList,
  },
  layout: 'projects',

  middleware: ['check-auth', 'auth'],

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
        singleClassClassification: false,
        allowOverlapping: false,
        graphemeMode: false,
        useRelation: false,
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
      } as ProjectWriteDTO,
      projects: {} as ProjectListDTO,
      selected: [] as ProjectDTO[],
      isLoading: false
    }
  },

  async fetch() {
    this.isLoading = true
    this.projects = await this.$services.project.list(this.$route.query)
    this.isLoading = false
  },

  computed: {
    ...mapGetters('auth', ['isStaff']),
    canDelete(): boolean {
      return this.selected.length > 0
    },
  },

  watch: {
    '$route.query': _.debounce(function() {
        // @ts-ignore
        this.$fetch()
      }, 1000
    ),
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

    updateQuery(query: object) {
      this.$router.push(query)
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
