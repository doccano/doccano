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
            <v-card-text class="title">
              {{ currentDoc.text }}
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
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'

export default {
  components: {
    LabelGroup,
    ListMetadata
  },
  layout: 'demo',

  data() {
    return {
      singleLabel: true,
      items: [
        {
          id: 4,
          text: 'Positive',
          prefixKey: null,
          suffixKey: 'p',
          backgroundColor: '#7c20e0',
          textColor: '#ffffff'
        },
        {
          id: 5,
          text: 'Negative',
          prefixKey: null,
          suffixKey: 'n',
          backgroundColor: '#fbb028',
          textColor: '#000000'
        }
      ],
      currentDoc: {
        id: 8,
        text: 'Fair drama/love story movie that focuses on the lives of blue collar people finding new life thru new love. The acting here is good but the film fails in cinematography, screenplay, directing and editing. The story/script is only average at best. This film will be enjoyed by Fonda and De Niro fans and by people who love middle age love stories where in the coartship is on a more wiser and cautious level. It would also be interesting for people who are interested on the subject matter regarding illiteracy.......',
        annotations: [
          {
            id: 17,
            prob: 0.0,
            label: 4,
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
