<template>
  <v-card>
    <v-card-title class="mb-2">
      <!-- <document-action-menu />
      <document-deletion-button class="ms-2" />
      <v-spacer />
      <document-bulk-deletion-button /> -->
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
import { DocumentListDTO, DocumentDTO } from '@/services/application/document.service'

export default Vue.extend({
  layout: 'project',

  components: {
    DocumentList,
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

  validate({ params, query }) {
    // @ts-ignore
    return /^\d+$/.test(params.id) && /^\d+|$/.test(query.limit) && /^\d+|$/.test(query.offset)
  }
})
</script>
