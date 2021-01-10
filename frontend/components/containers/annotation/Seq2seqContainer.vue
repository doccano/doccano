<template>
  <div>
    <v-card
      v-if="isReady"
      class="title mb-5"
    >
      <v-card-text class="title">
        {{ currentDoc.text }}
      </v-card-text>
    </v-card>
    <seq2seq-box
      v-if="isReady"
      :text="currentDoc.text"
      :annotations="currentDoc.annotations"
      :delete-annotation="_deleteAnnotation"
      :update-annotation="_updateAnnotation"
      :create-annotation="_createAnnotation"
    />
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import Seq2seqBox from '~/components/organisms/annotation/Seq2seqBox'

export default {
  components: {
    Seq2seqBox
  },

  computed: {
    ...mapState('documents', ['loading']),
    ...mapGetters('documents', ['currentDoc']),
    isReady() {
      return this.currentDoc && !this.loading
    }
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
        text,
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
