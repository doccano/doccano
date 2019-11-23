<template>
  <v-content>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
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
        </v-col>
        <v-col cols="12" md="3">
          <metadata-box :metadata="JSON.parse(currentDoc.meta)" />
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import MultiClassClassification from '~/components/organisms/annotation/MultiClassClassification'
import MetadataBox from '@/components/organisms/annotation/MetadataBox'

export default {
  layout: 'demo',

  components: {
    MultiClassClassification,
    MetadataBox
  },

  data() {
    return {
      items: [
        {
          id: 4,
          text: 'Positive',
          prefix_key: null,
          suffix_key: 'p',
          background_color: '#7c20e0',
          text_color: '#ffffff'
        },
        {
          id: 5,
          text: 'Negative',
          prefix_key: null,
          suffix_key: 'n',
          background_color: '#fbb028',
          text_color: '#000000'
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
        meta: '{"wikiPageId":2}',
        annotation_approver: null
      }
    }
  },

  methods: {
    removeLabel(annotationId) {
      this.currentDoc.annotations = this.currentDoc.annotations.filter(item => item.id !== annotationId)
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
