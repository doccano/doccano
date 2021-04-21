<template>
  <v-card>
    <v-card-title>
      <action-menu
        @upload="upload"
        @download="dialogDownload=true"
      />
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete=true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-spacer />
      <v-btn
        :disabled="!item.count"
        class="text-capitalize"
        color="error"
        @click="dialogDeleteAll=true"
      >
        {{ $t('generic.deleteAll') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          @cancel="dialogDelete=false"
          @remove="remove"
        />
      </v-dialog>
      <v-dialog v-model="dialogDeleteAll">
        <form-delete-bulk
          @cancel="dialogDeleteAll=false"
          @remove="removeAll"
        />
      </v-dialog>
      <v-dialog v-model="dialogDownload">
        <form-download
          @cancel="dialogDownload=false"
        />
      </v-dialog>
    </v-card-title>
    <document-list
      v-model="selected"
      :items="item.items"
      :is-loading="isLoading"
      :total="item.count"
      @update:query="updateQuery"
      @click:labeling="movePage"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'
import DocumentList from '@/components/document/DocumentList.vue'
import FormDelete from '@/components/document/FormDelete.vue'
import FormDeleteBulk from '@/components/document/FormDeleteBulk.vue'
import FormDownload from '@/components/document/FormDownload.vue'
import { DocumentListDTO, DocumentDTO } from '~/services/application/document/documentData'
import ActionMenu from '~/components/document/ActionMenu.vue'
import { ProjectDTO } from '~/services/application/project/projectData'

export default Vue.extend({
  layout: 'project',

  components: {
    ActionMenu,
    DocumentList,
    FormDelete,
    FormDeleteBulk,
    FormDownload,
  },

  async fetch() {
    this.isLoading = true
    this.item = await this.$services.document.list(this.projectId, this.$route.query)
    this.isLoading = false
  },

  data() {
    return {
      dialogDelete: false,
      dialogDeleteAll: false,
      dialogDownload: false,
      project: {} as ProjectDTO,
      item: {} as DocumentListDTO,
      selected: [] as DocumentDTO[],
      isLoading: false
    }
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId(): string {
      return this.$route.params.id
    }
  },

  watch: {
    '$route.query': _.debounce(function() {
        // @ts-ignore
        this.$fetch()
      }, 1000
    ),
  },

  async created() {
    this.project = await this.$services.project.findById(this.projectId)
  },

  methods: {
    async remove() {
      await this.$services.document.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },
    async removeAll() {
      await this.$services.document.bulkDelete(this.projectId, [])
      this.$fetch()
      this.dialogDeleteAll = false
      this.selected = []
    },
    upload() {
      this.$router.push(`/projects/${this.projectId}/upload`)
    },
    updateQuery(query: object) {
      this.$router.push(query)
    },
    movePage(query: object) {
      this.updateQuery({
        path: this.localePath(this.project.pageLink),
        query
      })
    }
  },

  validate({ params, query }) {
    // @ts-ignore
    return /^\d+$/.test(params.id) && /^\d+|$/.test(query.limit) && /^\d+|$/.test(query.offset)
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
