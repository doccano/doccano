<template>
  <v-card v-if="isReady" v-shortkey="multiKeys" @shortkey="addOrRemoveLabel">
    <v-card-title>
      <v-card-title>
        <multi-class-classification
          :labels="itemsl"
          :annotations="currentDoc.annotations"
          :add-label="addLabel"
          :delete-label="removeLabel"
        />
      </v-card-title>
      <v-card-text class="title highlight" v-text="currentDoc.text" />
    </v-card-title>
  </v-card>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapGetters, mapState } from 'vuex'
import MultiClassClassification from '@/components/organisms/annotation/MultiClassClassification'
Vue.use(require('vue-shortkey'))

export default {
  components: {
    MultiClassClassification
  },

  data(a) {
    return {
      L1: Object.assign({}, this.$store.state.items)
    }
  },

  getters: {
    lgetter: (state) => {
      return state.items.filter(it => !it.text.includes('/'))
    }
  },

  computed: {
    // ...mapState('labels', ['items']),
    ...mapState('documents', ['loading']),
    ...mapGetters('documents', ['currentDoc']),
    // ...mapGetters('labels', ['L1getter']),
    ...mapState('labels', {
      // items: 'items'
      items(state) {
        console.log('level1', state)

        return state.items.filter(it => !it.text.includes('/'))
      },
      itemsl(state) {
        let id
        if (this.currentDoc.annotations[0]) {
          id = this.currentDoc.annotations[0].label
        }

        let target
        state.items.map((it) => {
          if (it.id === id) {
            target = it.text
          }
        })
        console.log('Level2', target, id)
        if (target) {
          return state.items.filter(it => it.text.includes(target))
        } else {
          return state.items.filter(it => !it.text.includes('/'))
        }
      }
    }),
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
    this.getLabelList({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('labels', ['getLabelList']),
    ...mapActions('documents', [
      'getDocumentList',
      'deleteAnnotation',
      'updateAnnotation',
      'addAnnotation'
    ]),
    removeLabel(annotationId) {
      console.log('removeLabel id', annotationId)
      const payload = {
        annotationId,
        projectId: this.$route.params.id
      }
      this.deleteAnnotation(payload)
    },
    // updateLabel(labelId, annotationId) {
    //   console.log('updateLabel id', labelId)
    //   const payload = {
    //     annotationId,
    //     label: labelId,
    //     projectId: this.$route.params.id
    //   }
    //   this.updateAnnotation(payload)
    // },
    addLabel(labelId) {
      console.log('addLabel id', labelId)
      // this.$forceUpdate()
      const payload = {
        label: labelId,
        projectId: this.$route.params.id
      }

      let deleteId
      let innerId
      if (this.currentDoc.annotations[0]) {
        deleteId = this.currentDoc.annotations[0].id
        innerId = this.currentDoc.annotations[0].label
      }

      // const payloadDelete = {
      //   id,
      //   projectId: this.$route.params.id
      // }
      // this.deleteAnnotation(payloadDelete)
      const allLabel = [...this.items, ...this.itemsl]
      let newLabelText
      let labeledText
      allLabel.map((it) => {
        if (it.id === labelId) {
          newLabelText = it.text
        } else if (it.id === innerId) {
          labeledText = it.text
        }
      })
      console.log(newLabelText, labeledText)

      this.addAnnotation(payload)
      if (deleteId) {
        this.removeLabel(deleteId)
      }
      // if (!newLabelText.includes('/')) {
      //   if (deleteId) {
      //     this.removeLabel(deleteId)
      //   }
      // }
    },
    addOrRemoveLabel(event) {
      console.log('addOrRemoveLabel id', event)
      const label = this.items.find(
        item => item.id === parseInt(event.srcKey, 10)
      )
      const annotation = this.currentDoc.annotations.find(
        item => item.label === label.id
      )
      if (annotation) {
        this.removeLabel(annotation.id)
      } else {
        this.addLabel(label.id)
      }
    }
  }
}
</script>

<style scoped>
.highlight {
  white-space: pre-wrap;
}
</style>
