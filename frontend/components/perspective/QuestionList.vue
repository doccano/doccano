<template>
  <div>
    <div class="d-flex justify-end mb-3">
      <v-btn
        v-if="questions.length > 0"
        color="error"
        :disabled="loading"
        @click="$emit('delete-all')"
      >
        <v-icon left>{{ mdiDelete }}</v-icon>
        Delete Perspective
      </v-btn>
    </div>

    <v-data-table
      :headers="headers"
      :items="questions"
      :loading="loading"
      class="elevation-1"
      :items-per-page="10"
    >
      <template #[`item.question_type`]="{ item }">
        <v-chip
          :color="item.questionType === 'open' ? 'blue' : 'green'"
          text-color="white"
          small
        >
          {{ item.questionType === 'open' ? 'Open Text' : 'Multiple Choice' }}
        </v-chip>
      </template>

      <template #[`item.is_required`]="{ item }">
        <v-icon :color="item.isRequired ? 'success' : 'grey'">
          {{ item.isRequired ? mdiCheck : mdiClose }}
        </v-icon>
      </template>

      <template #[`item.answer_count`]="{ item }">
        <v-chip small>
          {{ item.answerCount }} answers
        </v-chip>
      </template>

      <template #[`item.actions`]="{ item }">
        <v-btn icon small @click="$emit('edit', item)">
          <v-icon>{{ mdiPencil }}</v-icon>
        </v-btn>
        <v-btn icon small color="error" @click="$emit('delete', item)">
          <v-icon>{{ mdiDelete }}</v-icon>
        </v-btn>
      </template>

      <template #[`item.text`]="{ item }">
        <div class="text-truncate" style="max-width: 300px;">
          {{ item.text }}
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { mdiPencil, mdiDelete, mdiCheck, mdiClose } from '@mdi/js'

export default {
  props: {
    questions: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      mdiPencil,
      mdiDelete,
      mdiCheck,
      mdiClose,
      headers: [
        {
          text: 'Order',
          value: 'order',
          width: '80px'
        },
        {
          text: 'Question',
          value: 'text',
          sortable: false
        },
        {
          text: 'Type',
          value: 'question_type',
          width: '150px'
        },
        {
          text: 'Required',
          value: 'is_required',
          width: '100px'
        },
        {
          text: 'Answers',
          value: 'answer_count',
          width: '120px'
        },
        {
          text: 'Actions',
          value: 'actions',
          sortable: false,
          width: '120px'
        }
      ]
    }
  }
}
</script>
