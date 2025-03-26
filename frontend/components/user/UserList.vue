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
    <template #[`item.isSuperUser`]="{ item }">
      <v-icon v-if="item.isSuperUser" color="primary">{{ mdiCheck }}</v-icon>
      <v-icon v-else>{{ mdiClose }}</v-icon>
    </template>
    <template #[`item.isStaff`]="{ item }">
      <v-icon v-if="item.isStaff" color="primary">{{ mdiCheck }}</v-icon>
      <v-icon v-else>{{ mdiClose }}</v-icon>
    </template>
    <template #[`item.isActive`]="{ item }">
      <v-icon v-if="item.isActive" color="primary">{{ mdiCheck }}</v-icon>
      <v-icon v-else>{{ mdiClose }}</v-icon>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify, mdiCheck, mdiClose } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import { User } from '~/domain/models/user/user'

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
      mdiCheck,
      mdiClose
    }
  },

  computed: {
    headers(): { text: any; value: string; sortable?: boolean; align?: string }[] {
      return [
        { text: this.$t('user.username'), value: 'username' },
        { text: this.$t('user.email'), value: 'email' },
        { text: this.$t('user.superUser'), value: 'isSuperUser', align: 'center' },
        { text: this.$t('user.staff'), value: 'isStaff', align: 'center' },
        { text: this.$t('user.active'), value: 'isActive' }
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
        payload.query.ordering = 'username'
        payload.query.orderBy = ''
      }
      this.$emit('update:query', payload)
    }
  }
})
</script>
