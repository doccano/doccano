<template>
  <div>
    <v-card
      v-if="currentDoc"
      class="title mb-5"
    >
      <v-card-text class="title">
        {{ currentDoc.text }}
      </v-card-text>
    </v-card>
    <seq2seq-box
      v-if="currentDoc"
      :text="currentDoc.text"
      :annotations="currentDoc.annotations"
      :delete-annotation="_deleteAnnotation"
      :update-annotation="_updateAnnotation"
      :create-annotation="_createAnnotation"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import Seq2seqBox from '~/components/organisms/annotation/Seq2seqBox'

export default {
  components: {
    Seq2seqBox
  },

  computed: {
    ...mapGetters('documents', ['currentDoc'])
  },

  methods: {
    ...mapActions('documents', ['getDocumentList', 'deleteAnnotation', 'updateAnnotation', 'addAnnotation']),
    _deleteAnnotation(annotationId) {
      const payload = {
        annotationId,
        projectId: this.$route.params.id
      }
      this.deleteAnnotation(payload)
    },
    _updateAnnotation(annotationId, text) {
      const payload = {
        annotationId,
        text: text,
        projectId: this.$route.params.id
      }
      this.updateAnnotation(payload)
    },
    _createAnnotation(text) {
      const payload = {
        text,
        projectId: this.$route.params.id
      }
      this.addAnnotation(payload)
    }
  }
}
</script>
