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

    <!-- Coluna Username -->
    <template #[`item.username`]="{ item }">
      <span>{{ item.username }}</span>
    </template>

    <!-- Coluna is_staff -->
    <template #[`item.is_staff`]="{ item }">
      <span>{{ item.is_staff ? $t('generic.yes') : $t('generic.no') }}</span>
    </template>

    <!-- Coluna is_superuser -->
    <template #[`item.is_superuser`]="{ item }">
      <span>{{ item.is_superuser ? $t('generic.yes') : $t('generic.no') }}</span>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import { User } from '~/domain/models/user'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      required: true
    },
    items: {
      type: Array as PropType<User[]>,
      required: true
    },
    value: {
      type: Array as PropType<User[]>,
      required: true
    },
    total: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      search: this.$route.query.q || '',
      options: {} as DataOptions,
      mdiMagnify
    }
  },
  computed: {
    headers(): { text: string; value: string; sortable?: boolean }[] {
      return [
        { text: this.$t('generic.username'), value: 'username' },
        { text: this.$t('generic.isStaff'), value: 'is_staff' },
        { text: this.$t('generic.isSuperuser'), value: 'is_superuser' }
      ]
    }
  },
  methods: {
    updateQuery(payload: any) {
      const { sortBy, sortDesc } = this.options
      if (sortBy && sortBy.length === 1 && sortDesc && sortDesc.length === 1) {
        payload.query.sortBy = sortBy[0]
        payload.query.sortDesc = sortDesc[0]
      } else {
        payload.query.sortBy = 'username'
        payload.query.sortDesc = false
      }
      this.$emit('update:query', payload)
    }
  }
})
</script>
