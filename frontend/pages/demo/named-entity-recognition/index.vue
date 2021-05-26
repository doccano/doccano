<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-card-text class="title">
              <entity-item-box
                :labels="items"
                :text="currentDoc.text"
                :entities="currentDoc.annotations"
                :delete-annotation="removeEntity"
                :update-entity="updateEntity"
                :add-entity="addEntity"
              />
            </v-card-text>
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
import EntityItemBox from '~/components/tasks/sequenceLabeling/EntityItemBox'

export default {
  layout: 'demo',

  components: {
    EntityItemBox,
    ListMetadata
  },

  data() {
    return {
      items: [
        {
          id: 4,
          text: 'LOC',
          prefixKey: null,
          suffixKey: 'l',
          backgroundColor: '#7c20e0',
          textColor: '#ffffff'
        },
        {
          id: 5,
          text: 'MISC',
          prefixKey: null,
          suffixKey: 'm',
          backgroundColor: '#fbb028',
          textColor: '#000000'
        },
        {
          id: 6,
          text: 'ORG',
          prefixKey: null,
          suffixKey: 'o',
          backgroundColor: '#e6d176',
          textColor: '#000000'
        },
        {
          id: 7,
          text: 'PER',
          prefixKey: null,
          suffixKey: 'p',
          backgroundColor: '#6a74b9',
          textColor: '#ffffff'
        }
      ],
      currentDoc: {
        id: 8,
        text: 'After bowling Somerset out for 83 on the opening morning at Grace Road , Leicestershire extended their first innings by 94 runs before being bowled out for 296 with England discard Andy Caddick taking three for 83 .',
        annotations: [
          {
            id: 17,
            prob: 0.0,
            label: 4,
            startOffset: 60,
            endOffset: 70,
            user: 1,
            document: 8
          },
          {
            id: 19,
            prob: 0.0,
            label: 4,
            startOffset: 165,
            endOffset: 172,
            user: 1,
            document: 8
          },
          {
            id: 16,
            prob: 0.0,
            label: 6,
            startOffset: 14,
            endOffset: 22,
            user: 1,
            document: 8
          },
          {
            id: 18,
            prob: 0.0,
            label: 6,
            startOffset: 73,
            endOffset: 87,
            user: 1,
            document: 8
          },
          {
            id: 20,
            prob: 0.0,
            label: 7,
            startOffset: 181,
            endOffset: 193,
            user: 1,
            document: 8
          }
        ],
        meta: { wikiPageId: 2 },
        annotation_approver: null
      }
    }
  },

  methods: {
    removeEntity(annotationId) {
      this.currentDoc.annotations = this.currentDoc.annotations.filter(item => item.id !== annotationId)
    },
    updateEntity(labelId, annotationId) {
      const index = this.currentDoc.annotations.findIndex(item => item.id === annotationId)
      this.currentDoc.annotations[index].label = labelId
    },
    addEntity(startOffset, endOffset, labelId) {
      const payload = {
        id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
        startOffset,
        endOffset,
        label: labelId
      }
      this.currentDoc.annotations.push(payload)
    }
  }
}
</script>
