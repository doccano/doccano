<template>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      'showFirstLastPage': true,
      'items-per-page-options': [5, 10, 15, 100],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="$emit('input', $event)"
  >
    <template v-slot:[`item.createdAt`]="{ item }">
      <span>{{ item.createdAt | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('DD/MM/YYYY HH:mm') }}</span>
    </template>
    <template v-slot:top>
      <v-text-field
        v-model="search"
        prepend-inner-icon="search"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <template v-slot:[`item.action`]="{ item }">
      <v-btn
        small
        color="primary text-capitalize"
        @click="toLabeling(item)"
      >
        {{ $t('dataset.annotate') }}
      </v-btn>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
import { CommentReadDTO } from '~/services/application/comment/commentData'
import { ExampleDTO } from '~/services/application/example/exampleData'
Vue.use(VueFilterDateFormat)
Vue.use(VueFilterDateParse)

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    examples: {
      type: Array as PropType<ExampleDTO[]>,
      default: () => [],
      required: true
    },
    items: {
      type: Array as PropType<CommentReadDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<CommentReadDTO[]>,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      search: '',
      headers: [
        { text: this.$t('dataset.text'), value: 'text' },
        { text: this.$t('user.username'), value: 'username' },
        { text: this.$t('comments.created_at'), value: 'createdAt' },
        { text: this.$t('dataset.action'), value: 'action' },
      ]
    }
  },

  methods: {
    toLabeling(item: CommentReadDTO) {
      const index = this.examples.findIndex((example: ExampleDTO) => example.id === item.example)
      const page = (index + 1).toString()
      this.$emit('click:labeling', { page, q: this.search })
    }
  }
})
</script>
