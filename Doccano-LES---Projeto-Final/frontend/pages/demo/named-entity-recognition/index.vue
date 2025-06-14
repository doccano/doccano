<template>
  <v-main>
    <v-container fluid>
      <div class="mb-2">
        <v-btn
          text
          outlined
          class="text-capitalize mr-2"
          @click="allowOverlapping = !allowOverlapping"
        >
          Overlapping({{ allowOverlapping }})
        </v-btn>
        <v-btn text outlined @click="rtl = !rtl">
          RTL(<span class="text-capitalize">{{ rtl }}</span
          >)
        </v-btn>
      </div>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <div class="annotation-text pa-4">
              <entity-editor
                :dark="$vuetify.theme.dark"
                :rtl="rtl"
                :text="currentDoc.text"
                :entities="currentDoc.annotations"
                :entity-labels="entityLabels"
                :relations="relations"
                :relation-labels="relationLabels"
                :allow-overlapping="allowOverlapping"
                @addEntity="addEntity"
                @click:entity="updateEntity"
                @contextmenu:entity="deleteEntity"
                @contextmenu:relation="deleteRelation"
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
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
export default {
  components: {
    EntityEditor,
    ListMetadata
  },
  layout: 'demo',
  data() {
    return {
      allowOverlapping: false,
      rtl: false,
      entityLabels: [
        {
          id: 4,
          text: 'LOC',
          prefixKey: null,
          suffixKey: 'l',
          color: '#7c20e0',
          textColor: '#ffffff'
        },
        {
          id: 5,
          text: 'MISC',
          prefixKey: null,
          suffixKey: 'm',
          color: '#fbb028',
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
          text: 'PER',
          prefixKey: null,
          suffixKey: 'p',
          color: '#6a74b9',
          textColor: '#ffffff'
        }
      ],
      relations: [
        {
          id: 0,
          fromId: 16,
          toId: 17,
          labelId: 0
        }
      ],
      relationLabels: [
        {
          id: 0,
          text: 'isLorem',
          color: '#ffffff'
        }
      ],
      currentDoc: {
        id: 8,
        text: 'After bowling Somerset out for 83 on the opening morning at Grace Road, Leicestershire extended their first innings by 94 runs before being bowled out for 296 with England discard Andy Caddick taking three for 83.',
        annotations: [
          {
            id: 17,
            prob: 0.0,
            label: 4,
            startOffset: 60,
            endOffset: 70,
            user: 1
          },
          {
            id: 19,
            prob: 0.0,
            label: 4,
            startOffset: 164,
            endOffset: 171,
            user: 1
          },
          {
            id: 16,
            prob: 0.0,
            label: 6,
            startOffset: 14,
            endOffset: 22,
            user: 1
          },
          {
            id: 18,
            prob: 0.0,
            label: 6,
            startOffset: 72,
            endOffset: 86,
            user: 1
          },
          {
            id: 20,
            prob: 0.0,
            label: 7,
            startOffset: 180,
            endOffset: 192,
            user: 1
          }
        ],
        meta: { wikiPageId: 2 },
        annotation_approver: null
      }
    }
  },
  watch: {
    rtl() {
      this.relations = []
      this.currentDoc.annotations = []
      // this.$vuetify.rtl = this.rtl
      if (this.rtl) {
        this.currentDoc.text = 'داستان SVG Tiny 1.2 طولا ني است.'
      } else {
        this.currentDoc.text =
          'After bowling Somerset out for 83 on the opening morning at Grace Road, Leicestershire extended their first innings by 94 runs before being bowled out for 296 with England discard Andy Caddick taking three for 83.'
      }
    }
  },
  methods: {
    deleteEntity(annotationId) {
      this.currentDoc.annotations = this.currentDoc.annotations.filter(
        (item) => item.id !== annotationId
      )
      this.relations.forEach((r) => {
        if (r.fromId === annotationId || r.toId === annotationId) {
          this.deleteRelation(r.id)
        }
      })
    },
    updateEntity(annotationId, labelId) {
      const index = this.currentDoc.annotations.findIndex((item) => item.id === annotationId)
      this.currentDoc.annotations[index].label = labelId
      this.currentDoc.annotations = [...this.currentDoc.annotations]
    },
    addEntity(startOffset, endOffset, labelId) {
      console.log(startOffset, endOffset, labelId)
      const payload = {
        id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
        startOffset,
        endOffset,
        label: labelId
      }
      this.currentDoc.annotations = [...this.currentDoc.annotations, payload]
    },
    deleteRelation(relationId) {
      this.relations = this.relations.filter((item) => item.id !== relationId)
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
  opacity: 0.8;
}
</style>
