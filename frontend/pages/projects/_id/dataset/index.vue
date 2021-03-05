<template>
  <v-card>
    <v-card-title>
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
    </v-card-title>
    <document-list
      v-model="selected"
      :items="item.items"
      :is-loading="isLoading"
      :page-link="pageLink"
      :total="item.count"
      @change-query="$fetch"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import DocumentList from '@/components/document/DocumentList.vue'
import FormDelete from '@/components/document/FormDelete.vue'
import FormDeleteBulk from '@/components/document/FormDeleteBulk.vue'
import { DocumentListDTO, DocumentDTO } from '@/services/application/document.service'

export default Vue.extend({
  layout: 'project',

  components: {
    DocumentList,
    FormDelete,
    FormDeleteBulk
  },

  async fetch() {
    this.isLoading = true
    this.item = await this.$services.document.list(this.projectId, this.$route.query)
    this.isLoading = false
  },

  data() {
    return {
      dialogCreate: false,
      dialogDelete: false,
      dialogDeleteAll: false,
      pageLink: '',
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

  async created() {
    this.pageLink = await this.$services.project.getPageLink(this.projectId)
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
