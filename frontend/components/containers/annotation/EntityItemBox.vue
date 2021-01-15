<template>
  <entity-item-box
    v-if="isReady"
    :labels="items"
    :text="currentDoc.text"
    :entities="currentDoc.annotations"
    :delete-annotation="removeEntity"
    :update-entity="updateEntity"
    :add-entity="addEntity"
  />
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import EntityItemBox from '~/components/organisms/annotation/EntityItemBox'

export default {
  components: {
    EntityItemBox
  },

  computed: {
    ...mapState('labels', ['items', 'loading']),
    ...mapGetters('documents', ['currentDoc']),
    isReady() {
      return !!this.currentDoc && !this.loading
    }
  },

  created() {
    this.getLabelList({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('labels', ['getLabelList']),
    ...mapActions('documents', ['getDocumentList', 'deleteAnnotation', 'updateAnnotation', 'addAnnotation']),
    removeEntity(annotationId) {
      const payload = {
        annotationId,
        projectId: this.$route.params.id
      }
      this.deleteAnnotation(payload)
    },
    updateEntity(labelId, annotationId) {
      const payload = {
        annotationId,
        label: labelId,
        projectId: this.$route.params.id
      }
      this.updateAnnotation(payload)
    },
    addEntity(startOffset, endOffset, labelId) {
      const payload = {
        start_offset: startOffset,
        end_offset: endOffset,
        label: labelId,
        projectId: this.$route.params.id
      }
      this.addAnnotation(payload)
    }
  }
}
</script>
