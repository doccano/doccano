<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-card-title>
              <label-group
                :labels="items"
                :annotations="categoryAnnotations"
                :single-label="exclusive"
                @add="addLabel"
                @remove="removeLabel"
              />
            </v-card-title>
            <v-divider />
            <div class="annotation-text pa-4">
              <entity-editor
                :dark="$vuetify.theme.dark"
                :text="currentDoc.text"
                :entities="currentDoc.annotations"
                :entity-labels="entityLabels"
                @addEntity="addEntity"
                @click:entity="updateEntity"
                @contextmenu:entity="deleteEntity"
              />
            </div>
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
import EntityEditor from '@/components/tasks/sequenceLabeling/EntityEditor.vue'
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'

export default {
  components: {
    EntityEditor,
    ListMetadata,
    LabelGroup
  },

  layout: 'demo',

  data() {
    return {
      entityLabels: [
        {
          id: 4,
          text: 'City',
          prefixKey: null,
          suffixKey: 'l',
          color: '#fbb028',
          textColor: '#ffffff'
        },
        {
          id: 5,
          text: 'MISC',
          prefixKey: null,
          suffixKey: 'm',
          color: '#7c20e0',
          textColor: '#000000'
        },
        {
          id: 6,
          text: 'ORG',
          prefixKey: null,
          suffixKey: 'o',
          color: '#e6d176',
          textColor: '#000000'
        },
        {
          id: 7,
          text: 'Time',
          prefixKey: null,
          suffixKey: 'p',
          color: '#6a74b9',
          textColor: '#ffffff'
        }
      ],
      items: [
        {
          id: 4,
          text: 'Flight',
          prefixKey: null,
          suffixKey: 'f',
          backgroundColor: '#7c20e0',
          textColor: '#ffffff'
        },
        {
          id: 5,
          text: 'FlightTime',
          prefixKey: null,
          suffixKey: 't',
          backgroundColor: '#fbb028',
          textColor: '#000000'
        },
        {
          id: 6,
          text: 'Airfare',
          prefixKey: null,
          suffixKey: 'a',
          backgroundColor: '#1e90ff',
          textColor: '#000000'
        }
      ],
      categoryAnnotations: [
        {
          id: 17,
          prob: 0.0,
          label: 4,
          user: 1,
          document: 8
        }
      ],
      exclusive: true,
      currentDoc: {
        id: 8,
        text: 'I want to fly from Boston at 8:38 am and arrive in Denver at 11:10 in the morning.',
        annotations: [
          {
            id: 17,
            prob: 0.0,
            label: 4,
            startOffset: 19,
            endOffset: 25,
            user: 1
          },
          {
            id: 19,
            prob: 0.0,
            label: 7,
            startOffset: 29,
            endOffset: 36,
            user: 1
          },
          {
            id: 16,
            prob: 0.0,
            label: 4,
            startOffset: 51,
            endOffset: 57,
            user: 1
          },
          {
            id: 18,
            prob: 0.0,
            label: 7,
            startOffset: 61,
            endOffset: 66,
            user: 1
          }
        ],
        meta: { wikiPageId: 2 },
        annotation_approver: null
      }
    }
  },

  methods: {
    deleteEntity(annotationId) {
      this.currentDoc.annotations = this.currentDoc.annotations.filter(
        (item) => item.id !== annotationId
      )
    },

    updateEntity(annotationId, labelId) {
      const index = this.currentDoc.annotations.findIndex((item) => item.id === annotationId)
      this.currentDoc.annotations[index].label = labelId
      this.currentDoc.annotations = [...this.currentDoc.annotations]
    },

    addEntity(startOffset, endOffset, labelId) {
      const payload = {
        id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
        startOffset,
        endOffset,
        label: labelId
      }
      this.currentDoc.annotations = [...this.currentDoc.annotations, payload]
    },

    removeLabel(annotationId) {
      this.categoryAnnotations = this.categoryAnnotations.filter((item) => item.id !== annotationId)
    },

    addLabel(labelId) {
      const payload = {
        id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
        label: labelId
      }
      this.categoryAnnotations.push(payload)
    }
  }
}
</script>
<style scoped>
.annotation-text {
  font-size: 1.25rem !important;
  font-weight: 500;
  line-height: 2rem;
  font-family: 'Roboto', sans-serif !important;
  opacity: 0.6;
}
</style>
