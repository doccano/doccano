<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-card-title>
              <label-group
                :labels="items"
                :annotations="currentDoc.annotations"
                :single-label="singleLabel"
                @add="addLabel"
                @remove="removeLabel"
              />
            </v-card-title>
            <v-divider />
            <v-img contain :src="currentDoc.filename" max-height="300" class="grey lighten-2" />
          </v-card>
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
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'

export default {
  components: {
    LabelGroup,
    ListMetadata
  },
  layout: 'demo',

  data() {
    return {
      items: [
        {
          id: 4,
          text: 'Cat',
          prefixKey: null,
          suffixKey: 'c',
          backgroundColor: '#7c20e0',
          textColor: '#ffffff'
        },
        {
          id: 5,
          text: 'Dog',
          prefixKey: null,
          suffixKey: 'd',
          backgroundColor: '#fbb028',
          textColor: '#000000'
        }
      ],
      singleLabel: true,
      currentDoc: {
        id: 8,
        filename: require('~/assets/images/demo/cat.jpeg'),
        annotations: [
          {
            id: 17,
            prob: 0.0,
            label: 4,
            user: 1,
            document: 8
          }
        ],
        meta: {
          url: 'https://github.com/Hironsan'
        },
        annotation_approver: null
      }
    }
  },

  methods: {
    removeLabel(annotationId) {
      this.currentDoc.annotations = this.currentDoc.annotations.filter(
        (item) => item.id !== annotationId
      )
    },
    addLabel(labelId) {
      const payload = {
        id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
        label: labelId
      }
      this.currentDoc.annotations.push(payload)
    }
  }
}
</script>
