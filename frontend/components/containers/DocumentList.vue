<template>
  <document-list
    :headers="headers"
    :docs="items"
    :selected="selected"
    @update-selected="updateSelected"
    @update-doc="handleUpdateDoc"
  />
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'
import DocumentList from '@/components/organisms/DocumentList'

export default {
  components: {
    DocumentList
  },
  data() {
    return {
      headers: [
        {
          text: 'Text',
          align: 'left',
          value: 'text'
        }
      ]
    }
  },

  computed: {
    ...mapState('documents', ['items', 'selected'])
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
