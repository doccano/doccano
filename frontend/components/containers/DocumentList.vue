<template>
  <document-list
    :headers="headers"
    :docs="items"
    :selected="selected"
    :loading="loading"
    @update-selected="updateSelected"
    @update-doc="handleUpdateDoc"
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
    ...mapState('documents', ['items', 'selected', 'loading']),
    ...mapGetters('documents', ['headers'])
  },

  created() {
    this.getDocumentList()
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
    }
  }
}
</script>
