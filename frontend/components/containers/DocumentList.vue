<template>
  <document-list
    :headers="headers"
    :docs="items"
    :selected="selected"
    :loading="loading"
    :total="total"
    @update-selected="updateSelected"
    @update-doc="handleUpdateDoc"
    @change-option="handleChangeOption"
  />
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'
import DocumentList from '@/components/organisms/DocumentList'

export default {
  components: {
    DocumentList
  },

  computed: {
    ...mapState('documents', ['items', 'selected', 'loading', 'total']),
    ...mapGetters('documents', ['headers'])
  },

  created() {
    this.getDocumentList({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('documents', ['getDocumentList', 'updateDocument']),
    ...mapMutations('documents', ['updateSelected']),

    handleUpdateDoc(payload) {
      const data = {
        projectId: this.$route.params.id,
        ...payload
      }
      this.updateDocument(data)
    },

    handleChangeOption(option) {
      this.getDocumentList({
        projectId: this.$route.params.id,
        limit: option.itemsPerPage,
        offset: (option.page - 1) * option.itemsPerPage
      })
    }
  }
}
</script>
