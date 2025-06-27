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
    <template #[`item.name`]="{ item }">
      <nuxt-link :to="localePath(`/groups/${item.id}`)">
        <span>{{ item.name }}</span>
      </nuxt-link>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import { Group } from '~/domain/models/group/group'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<Group[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<Group[]>,
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
      mdiMagnify
    }
  },

  computed: {
    headers(): { text: any; value: string; sortable?: boolean; align?: string }[] {
      return [
          { text: this.$t('group.name'), value: 'name' },
          { text: this.$t('group.id'), value: 'id' }
      ]
    }
  },

  watch: {
    options: {
      handler() {
        this.updateQuery({
          query: {
            limit: this.options.itemsPerPage?.toString(),
            offset: ((this.options.page ?? 1) - 1) * (this.options.itemsPerPage ?? 10),
            q: this.search
          }
        })
      },
      deep: true
    },
    search() {
      this.updateQuery({
        query: {
          limit: this.options.itemsPerPage?.toString(),
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
      if (sortBy && sortDesc && sortBy.length === 1 && sortDesc.length === 1) {
        payload.query.ordering = sortBy[0]
        payload.query.orderBy = sortDesc[0] ? '-' : ''
      } else {
        payload.query.ordering = 'name'
        payload.query.orderBy = ''
      }
      this.$emit('update:query', payload)
    }
  }
})
</script>
