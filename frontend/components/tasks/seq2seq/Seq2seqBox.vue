<template>
  <v-card>
    <v-data-table
      :headers="headers"
      :items="annotations"
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
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiPencil, mdiDeleteOutline } from '@mdi/js'

export default Vue.extend({
  props: {
    annotations: {
      type: Array,
      default: () => [],
      required: true
    }
  },

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
      mdiDeleteOutline
    }
  },

  methods: {
    update(annotationId: number, text: string) {
      if (text.length > 0) {
        this.$emit('update:annotation', annotationId, text)
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
        this.$emit('create:annotation', this.newText)
        this.newText = ''
      }
    },
    remove(annotationId: number) {
      this.$emit('delete:annotation', annotationId)
    },
    compositionStart() {
      this.isComposing = true
    },
    compositionEnd() {
      this.isComposing = false
      this.hasCompositionJustEnded = true
    }
  }
})
</script>
