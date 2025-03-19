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
    <template #[`item.username`]="{ item }">
      <nuxt-link :to="localePath(`/users/${item.id}`)">
        <span>{{ item.username }}</span>
      </nuxt-link>
    </template>
    <template #[`item.email`]="{ item }">
      <span>{{ item.email }}</span>
    </template>
    <template #[`item.createdAt`]="{ item }">
      <span>{{
        dateFormat(dateParse(item.createdAt, 'YYYY-MM-DDTHH:mm:ss'), 'YYYY/MM/DD HH:mm')
      }}</span>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import { dateFormat } from '@vuejs-community/vue-filter-date-format'
import { dateParse } from '@vuejs-community/vue-filter-date-parse'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import User from '~/domain/models/user/user'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<User[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<User[]>,
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
      search: this.$route.query.q,
      options: {} as DataOptions,
      mdiMagnify,
      dateFormat,
      dateParse
    }
  },

  computed: {
    headers(): { text: any; value: string; sortable?: boolean }[] {
      return [
        { text: 'Username', value: 'username' },
        { text: 'Email', value: 'email' },
        { text: 'Created At', value: 'createdAt' }
      ]
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
})
</script>