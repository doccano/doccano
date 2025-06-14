<template>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :options.sync="options"
    :server-items-length="total"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      showFirstLastPage: true,
      'items-per-page-options': [10, 50, 100],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="$emit('input', $event)"
  >
    <template #[`item.createdAt`]="{ item }">
      <span>{{
        item.createdAt | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('DD/MM/YYYY HH:mm')
      }}</span>
    </template>
    <template #top>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <!--
    Tempolary removing due to the performance
    <template #[`item.action`]="{ item }">
      <v-btn
        small
        color="primary text-capitalize"
        @click="toLabeling(item)"
      >
        {{ $t('dataset.annotate') }}
      </v-btn>
    </template> -->
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import { CommentItem } from '~/domain/models/comment/comment'
Vue.use(VueFilterDateFormat)
Vue.use(VueFilterDateParse)

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<CommentItem[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<CommentItem[]>,
      default: () => [],
      required: true
    },
    total: {
      type: Number,
      default: 0,
      required: true
    }
  },

  data() {
    return {
      search: '',
      options: {} as DataOptions,
      headers: [
        { text: this.$t('dataset.text'), value: 'text', sortable: false },
        { text: this.$t('user.username'), value: 'username', sortable: false },
        { text: this.$t('comments.created_at'), value: 'createdAt', sortable: false },
        { text: this.$t('dataset.action'), value: 'action', sortable: false },
        { text: this.$t('comments.document'), value: 'example' }
      ],
      mdiMagnify
    }
  },

  watch: {
    options: {
      handler() {
        this.updateQuery({
          query: {
            limit: this.options.itemsPerPage.toString(),
            offset: ((this.options.page - 1) * this.options.itemsPerPage).toString(),
            q: this.search
          }
        })
      },
      deep: true
    },
    search() {
      this.updateQuery({
        query: {
          limit: this.options.itemsPerPage.toString(),
          offset: '0',
          q: this.search
        }
      })
      this.options.page = 1
    }
  },

  methods: {
    updateQuery(payload: any) {
      const { sortBy, sortDesc } = this.options
      if (sortBy.length === 1 && sortDesc.length === 1) {
        payload.query.sortBy = sortBy[0]
        payload.query.sortDesc = sortDesc[0]
      } else {
        payload.query.sortBy = 'createdAt'
        payload.query.sortDesc = true
      }
      this.$emit('update:query', payload)
    }
  }

  // methods: {
  //   toLabeling(item: CommentReadDTO) {
  //     const index = this.examples.findIndex((example: ExampleDTO) => example.id === item.example)
  //     const page = (index + 1).toString()
  //     this.$emit('click:labeling', { page, q: this.search })
  //   }
  // }
})
</script>
