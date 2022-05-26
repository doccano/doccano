<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-img contain :src="currentDoc.filename" max-height="300" class="grey lighten-2" />
          </v-card>
          <seq2seq-box
            :annotations="annotations"
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
    ListMetadata,
    Seq2seqBox
  },
  layout: 'demo',

  data() {
    return {
      annotations: [
        {
          id: 17,
          text: 'A cat is looking up.',
          user: 1,
          document: 8
        },
        {
          id: 18,
          text: 'A cat is trying to climb the wall.',
          user: 1,
          document: 8
        }
      ],
      singleLabel: true,
      currentDoc: {
        id: 8,
        filename: require('~/assets/1500x500.jpeg'),
        meta: {
          url: 'https://github.com/Hironsan'
        },
        annotation_approver: null
      }
    }
  },

  methods: {
    _deleteAnnotation(annotationId) {
      this.annotations = this.annotations.filter((item) => item.id !== annotationId)
    },
    _updateAnnotation(annotationId, text) {
      const index = this.annotations.findIndex((item) => item.id === annotationId)
      this.annotations[index].text = text
    },
    _createAnnotation(text) {
      const payload = {
        id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
        text
      }
      this.annotations.push(payload)
    }
  }
}
</script>
