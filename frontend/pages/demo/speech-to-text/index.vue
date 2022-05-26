<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <audio controls :src="src" class="mt-2 mb-5" style="width: 100%">
            Your browser does not support the
            <code>audio</code> element.
          </audio>
          <seq2seq-box
            :text="currentDoc.text"
            :annotations="currentDoc.annotations"
            @delete:annotation="_deleteAnnotation"
            @update:annotation="_updateAnnotation"
            @create:annotation="_createAnnotation"
          />
        </v-col>
        <v-col cols="12" md="3">
          <list-metadata :metadata="currentDoc.meta" />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import Seq2seqBox from '~/components/tasks/seq2seq/Seq2seqBox'

export default {
  components: {
    Seq2seqBox,
    ListMetadata
  },
  layout: 'demo',

  data() {
    return {
      currentDoc: {
        id: 8,
        text: '',
        annotations: [
          {
            id: 17,
            text: 'Hi! Welcome to doccano!',
            user: 1,
            document: 8
          }
        ],
        meta: {
          url: 'https://github.com/doccano'
        },
        annotation_approver: null
      },
      src: require('~/assets/examples/speech_1.mp3').default
    }
  },

  methods: {
    _deleteAnnotation(annotationId) {
      this.currentDoc.annotations = this.currentDoc.annotations.filter(
        (item) => item.id !== annotationId
      )
    },
    _updateAnnotation(annotationId, text) {
      const index = this.currentDoc.annotations.findIndex((item) => item.id === annotationId)
      this.currentDoc.annotations[index].text = text
    },
    _createAnnotation(text) {
      const payload = {
        id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
        text
      }
      this.currentDoc.annotations.push(payload)
    }
  }
}
</script>
