<template>
  <base-text-area>
    <template #title>
      <multi-class-classification
        v-if="currentDoc"
        :labels="items"
        :annotations="currentDoc.annotations"
        :add-label="addLabel"
        :delete-label="removeLabel"
      />
    </template>
    <template #content>
      <div v-if="currentDoc" class="title">
        {{ currentDoc.text }}<!-- {{currentDoc}}-->
      </div>
    </template>
  </base-text-area>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import BaseTextArea from '@/components/molecules/BaseTextArea'
import MultiClassClassification from '@/components/organisms/MultiClassClassification'

export default {
  components: {
    BaseTextArea,
    MultiClassClassification
  },

  computed: {
    ...mapState('labels', ['items']),
    ...mapGetters('documents', ['currentDoc'])
  },

  created() {
    this.getLabelList()
    this.getDocumentList({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('labels', ['getLabelList']),
    ...mapActions('documents', ['getDocumentList', 'deleteAnnotation', 'updateAnnotation', 'addAnnotation']),
    removeLabel(annotationId) {
      const payload = {
        annotationId,
        projectId: this.$route.params.id
      }
      this.deleteAnnotation(payload)
    },
    updateLabel(labelId, annotationId) {
      const payload = {
        annotationId,
        label: labelId,
        projectId: this.$route.params.id
      }
      this.updateAnnotation(payload)
    },
    addLabel(labelId) {
      alert(labelId)
      const payload = {
        label: labelId,
        projectId: this.$route.params.id
      }
      this.addAnnotation(payload)
    }
  }
}
</script>
