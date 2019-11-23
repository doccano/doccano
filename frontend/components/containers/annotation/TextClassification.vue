<template>
  <v-card>
    <v-card-title>
      <multi-class-classification
        v-if="currentDoc"
        :labels="items"
        :annotations="currentDoc.annotations"
        :add-label="addLabel"
        :delete-label="removeLabel"
      />
    </v-card-title>
    <v-card-text v-if="currentDoc" class="title">
      {{ currentDoc.text }}
    </v-card-text>
  </v-card>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import MultiClassClassification from '@/components/organisms/annotation/MultiClassClassification'

export default {
  components: {
    MultiClassClassification
  },

  computed: {
    ...mapState('labels', ['items']),
    ...mapGetters('documents', ['currentDoc'])
  },

  created() {
    this.getLabelList({
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
      const payload = {
        label: labelId,
        projectId: this.$route.params.id
      }
      this.addAnnotation(payload)
    }
  }
}
</script>
