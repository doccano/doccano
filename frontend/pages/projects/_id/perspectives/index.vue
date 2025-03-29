<template>
  <v-card>
    <v-card-title>
      <v-btn class="text-capitalize ms-2" color="primary" @click="goToAdd">
        {{ $t('generic.add') }}
      </v-btn>

      <v-btn class="text-capitalize ms-2" :disabled="!canDelete" outlined
      @click.stop="dialogDelete = true">
        {{ $t('generic.delete') }}
      </v-btn>

      <v-dialog v-model="dialogDelete" max-width="600px">
        <form-delete-perspective
          :selected="selected"
          @cancel="dialogDelete = false"
          @remove="remove"
        />
      </v-dialog>
    </v-card-title>

    <v-card-text>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
      <v-data-table
        :headers="headers"
        :items="items"
        :options.sync="options"
        :server-items-length="total"
        :search="search"
        :loading="isLoading"
        :loading-text="$t('generic.loading')"
        :no-data-text="$t('perspectives.noDataAvailable') || 'No perspectives available'"
        :footer-props="{
          showFirstLastPage: true,
          'items-per-page-options': [10, 50, 100],
          'items-per-page-text': $t('vuetify.itemsPerPageText'),
          'page-text': $t('dataset.pageText')
        }"
        item-key="id"
        show-select
        v-model="selected"
      >
        <template v-slot:[`item.createdAt`]="{ item }">
          <span>
            {{ item.createdAt }}
          </span>
        </template>
        <template v-slot:[`item.user`]="{ item }">
          <span v-if="item && item.user">{{ item.user.username }}</span>
          <span v-else>N/A</span>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
import Vue from 'vue'
import axios from 'axios'
import { DataOptions } from 'vuetify/types'
import { PerspectiveItem } from '@/domain/models/perspective/perspective'

function toModel(item: any): PerspectiveItem {
  return {
    ...item
    // map fields if needed
  }
}

Vue.use(VueFilterDateFormat)
Vue.use(VueFilterDateParse)

export default Vue.extend({
  name: 'PerspectivesTable',
  layout: 'project',
  data() {
    return {
      form: {
        category: '',
        text: '',
      },
      dialogDelete: false,
      selected: [] as PerspectiveItem[],
      search: '',
      options: {
        page: 1,
        itemsPerPage: 10,
        sortBy: ['createdAt'],
        sortDesc: [true],
      } as DataOptions,
      headers: [
        { text: this.$t('perspectives.category') || 'Category', value: 'category', sortable: true },
        { text: this.$t('perspectives.context'), value: 'context', sortable: false },
        { text: this.$t('perspectives.submittedBy'), value: 'user', sortable: false },
        { text: this.$t('perspectives.createdAt'), value: 'createdAt', sortable: true },
      ],
      mdiMagnify,
      items: [] as PerspectiveItem[],
      total: 0,
      isLoading: false,
    };
  },
  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    }
  },
  methods: {
    goToAdd() {
      const projectId = this.$route.params.id
      this.$router.push(this.localePath(`/projects/${projectId}/perspectives/add`))
    },
    remove() {
      this.$emit('remove', this.selected)
      this.dialogDelete = false
      this.selected = []
    },
    async list(projectId: string, query?: any): Promise<PerspectiveItem[]> {
      const url = `/projects/${projectId}/perspectives`
      const response = await axios.get(url, { params: query })
      return response.data.map((item: any) => toModel(item))
    },
    fetchPerspectives() {
      const projectId = this.$route.params.id;
      const query: any = {
        limit: this.options.itemsPerPage || 10,
        offset: ((this.options.page ? this.options.page - 1 : 0)
        * (this.options.itemsPerPage || 10))
      };
      if (this.search) {
        query.q = this.search;
      }
      this.isLoading = true;
      this.$repositories.perspective.list(projectId)
        .then((data: any) => {
          console.log('API Response:', data);
          this.items = data.results || data;
          this.total = data.count || this.items.length;
        })
        .catch((error: any) => {
          console.error('Error fetching perspectives:', error.response || error.message);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    updateQuery() {
      this.fetchPerspectives()
    },
    submitPerspective() {
      const projectId = Number(this.$route.params.id); // Convert to number
      this.$repositories.perspective.create(projectId, this.form)
        .then(() => {
          this.$router.push(this.localePath(`/projects/${projectId}/perspectives`));
        })
        .catch((error: any) => {
          console.error('Error submitting perspective:', error);
        });
    }
  },
  watch: {
    options: {
      handler() {
        this.updateQuery()
      },
      deep: true
    },
    search() {
      this.options.page = 1
      this.updateQuery()
    }
  },
  mounted() {
    this.fetchPerspectives()
  }
})
</script>

<style scoped>
/* Add any custom styles if needed */
</style>