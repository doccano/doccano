<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="9">
          <v-card>
            <v-img contain :src="currentDoc.filename" max-height="300" class="grey lighten-2" />
          </v-card>
          <v-card>
            <v-data-table
              :headers="headers"
              :items="currentDoc.annotations"
              item-key="id"
              hide-default-header
              hide-default-footer
              disable-pagination
              class="elevation-1"
              @input="update"
            >
              <template #top>
                <v-text-field
                  v-model="newText"
                  :prepend-inner-icon="mdiPencil"
                  :label="$t('annotation.newText')"
                  autofocus
                  single-line
                  hide-details
                  filled
                  @keyup.enter="create"
                  @compositionstart="compositionStart"
                  @compositionend="compositionEnd"
                />
              </template>
              <template #[`item.text`]="{ item }">
                <v-edit-dialog>
                  <span class="title" style="font-weight: 400">
                    {{ item.text }}
                  </span>
                  <template #input>
                    <v-textarea
                      :value="item.text"
                      :label="$t('generic.edit')"
                      autofocus
                      @change="update(item.id, $event)"
                    />
                  </template>
                </v-edit-dialog>
              </template>
              <template #[`item.action`]="{ item }">
                <v-icon small @click="remove(item.id)">
                  {{ mdiDeleteOutline }}
                </v-icon>
              </template>
            </v-data-table>
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
import { mdiPencil, mdiDeleteOutline } from '@mdi/js'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'

export default {
  components: {
    ListMetadata
  },
  layout: 'demo',

  data() {
    return {
      newText: '',
      headers: [
        {
          text: 'Text',
          align: 'left',
          value: 'text'
        },
        {
          text: 'Actions',
          align: 'right',
          value: 'action'
        }
      ],
      isComposing: false,
      hasCompositionJustEnded: false,
      mdiPencil,
      mdiDeleteOutline,
      currentDoc: {
        id: 8,
        filename: require('~/assets/images/demo/cat.jpeg'),
        annotations: [
          {
            id: 17,
            text: 'A cat playing with flowers',
            user: 1,
            document: 8
          },
          {
            id: 18,
            text: 'A flower is blooming on the ground',
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
    update(annotationId, text) {
      if (text.length > 0) {
        const index = this.currentDoc.annotations.findIndex((item) => item.id === annotationId)
        this.currentDoc.annotations[index].text = text
      } else {
        this.remove(annotationId)
      }
    },
    create() {
      if (this.isComposing || this.hasCompositionJustEnded) {
        this.hasCompositionJustEnded = false
        return
      }
      if (this.newText.length > 0) {
        const payload = {
          id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
          text: this.newText
        }
        this.currentDoc.annotations.push(payload)
        this.newText = ''
      }
    },
    remove(annotationId) {
      this.currentDoc.annotations = this.currentDoc.annotations.filter(
        (item) => item.id !== annotationId
      )
    },
    compositionStart() {
      this.isComposing = true
    },
    compositionEnd() {
      this.isComposing = false
      this.hasCompositionJustEnded = true
    }
  }
}
</script>
