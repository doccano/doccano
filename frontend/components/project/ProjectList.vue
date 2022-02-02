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
      'showFirstLastPage': true,
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
      <nuxt-link :to="localePath(`/projects/${item.id}`)">
        <span>{{ item.name }}</span>
      </nuxt-link>
    </template>
    <template #[`item.updatedAt`]="{ item }">
      <span>{{ item.updatedAt | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('DD/MM/YYYY HH:mm') }}</span>
    </template>
    <template #[`item.tags`]="{ item }">
      <v-chip
        v-for="tag in item.tags"
        :key="tag.id"
        outlined v-text="tag.text"
      />
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { mdiMagnify } from '@mdi/js'
import { DataOptions } from 'vuetify/types'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
import { ProjectDTO } from '~/services/application/project/projectData'
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
      type: Array as PropType<ProjectDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<ProjectDTO[]>,
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
    headers() {
      return [
        { text: this.$t('generic.name'), value: 'name' },
        { text: this.$t('generic.description'), value: 'description' },
        { text: this.$t('generic.type'), value: 'projectType' },
        { text: 'Updated', value: 'updatedAt' },
        { text: 'Tags', value: 'tags'}
      ]
    }
  },

  watch: {
    options: {
      handler() {
        const self: any = this
        self.updateQuery({
          query: {
            limit: self.options.itemsPerPage.toString(),
            offset: ((self.options.page - 1) * self.options.itemsPerPage).toString(),
            q: self.search
          }
        })
      },
      deep: true
    },
    search() {
      const self: any = this
      self.updateQuery({
        query: {
          limit: self.options.itemsPerPage.toString(),
          offset: '0',
          q: self.search
        }
      })
      self.options.page = 1
    }
  },

  methods: {
    updateQuery(payload: any) {
      this.$emit('update:query', payload)
    }
  }
})
</script>
