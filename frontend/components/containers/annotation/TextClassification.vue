<template>
  <v-card
    v-if="isReady"
    v-shortkey="multiKeys"
    @shortkey="addOrRemoveLabel"
  >
    <v-card-title>
      <multi-class-classification
        :labels="items"
        :annotations="currentDoc.annotations"
        :add-label="addLabel"
        :delete-label="removeLabel"
      />
    </v-card-title>
    <v-card-text class="title">
      {{ currentDoc.text }}
    </v-card-text>
  </v-card>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
import MultiClassClassification from '@/components/organisms/annotation/MultiClassClassification'
Vue.use(require('vue-shortkey'))

export default {
  components: {
    MultiClassClassification
  },

  computed: {
    ...mapState('labels', ['items']),
    ...mapState('documents', ['loading']),
    ...mapGetters('documents', ['currentDoc']),
    ...mapGetters('pagination', ['offset']),
    multiKeys() {
      const multiKeys = {}
      for (const item of this.items) {
        multiKeys[item.id] = [item.suffix_key]
      }
      return multiKeys
    },
    isReady() {
      return this.currentDoc && this.items && !this.loading
    }
  },

  created() {
    this.updateSearchOptions({
      offset: this.offset
    })
    this.getDocumentList({
      projectId: this.$route.params.id
    })
    this.getLabelList({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('labels', ['getLabelList']),
    ...mapActions('documents', ['getDocumentList', 'deleteAnnotation', 'updateAnnotation', 'addAnnotation']),
    ...mapMutations('documents', ['updateSearchOptions']),
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
    },
    addOrRemoveLabel(event) {
      const label = this.items.find(item => item.id === parseInt(event.srcKey, 10))
      const annotation = this.currentDoc.annotations.find(item => item.label === label.id)
      if (annotation) {
        this.removeLabel(annotation.id)
      } else {
        this.addLabel(label.id)
      }
    }
  }
}
</script>
