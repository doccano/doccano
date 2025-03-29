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
        v-model="selected"
        :headers="headers"
        :items="items"
        :options.sync="options"
        :server-items-length="total"
        :search="search"
        :loading="isLoading"
        :loading-text="$t('generic.loading')"
        :no-data-text="$t('perspectives.noDataAvailable') || 'No perspectives available'"
        :footer-props="tableFooterProps"
        show-select
        item-key="id"
      >
        <template slot="item.user" slot-scope="props">
          <span v-if="props.item && props.item.user && props.item.user.username">
            {{ props.item.user.username }}
          </span>
          <span v-else>
            {{ props.item.user ? 'User ' + props.item.user : 'N/A' }}
          </span>
        </template>
        <template slot="item.createdAt" slot-scope="props">
          <span>{{ formatTime(props.item.createdAt) }}</span>
        </template>
        <template slot="item.updatedAt" slot-scope="props">
          <span>{{ formatTime(props.item.updatedAt) }}</span>
        </template>
        <template slot="item.category" slot-scope="props">
          <span>{{ props.item.category }}</span>
        </template>
        <template slot="item.subject" slot-scope="props">
          <span>{{ props.item.subject }}</span>
        </template>
        <template slot="item.text" slot-scope="props">
          <span>{{ props.item.text }}</span>
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
    id: item.id || 'N/A',
    userId: item.user || 'N/A',
    projectId: item.project || 'N/A',
    subject: item.subject || 'N/A',
    category: item.category || 'N/A',
    text: item.text || 'N/A',
    createdAt: item.created_at || item.createdAt || 'N/A',
    updatedAt: item.updated_at || item.updatedAt || 'N/A',
  };
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
        subject: '',
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
        { text: this.$t('Submitted By') || 'Submitted By', value: 'user', sortable: false },
        { text: this.$t('Created At') || 'Created At', value: 'createdAt', sortable: true },
        { text: this.$t('Updated At') || 'Updated At', value: 'updatedAt', sortable: true },
        { text: this.$t('Category') || 'Category', value: 'category', sortable: true },
        { text: this.$t('Subject') || 'Subject', value: 'subject', sortable: true },
        { text: this.$t('Text') || 'Text', value: 'text', sortable: false },
      ],
      mdiMagnify,
      items: [] as PerspectiveItem[],
      total: 0,
      isLoading: false,
    }
  },
  computed: {
    canDelete(): boolean {
      return this.selected.length > 0;
    },
    tableFooterProps() {
      return {
        showFirstLastPage: true,
        'items-per-page-options': [10, 50, 100],
        'items-per-page-text': this.$t('vuetify.itemsPerPageText'),
        'page-text': this.$t('dataset.pageText')
      }
    }
  },
  methods: {
    goToAdd() {
      const projectId = this.$route.params.id;
      this.$router.push(this.localePath(`/projects/${projectId}/perspectives/add`));
    },
    remove() {
      this.$emit('remove', this.selected);
      this.dialogDelete = false;
      this.selected = [];
    },
    async list(projectId: string, query?: any): Promise<PerspectiveItem[]> {
      const url = `/projects/${projectId}/perspectives`;
      const response = await axios.get(url, { params: query });
      return response.data.map((item: any) => toModel(item));
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
      this.$repositories.perspective.list(projectId, query)
        .then((data: any) => {
          console.log('API Response:', data); // Log the raw API response
          const items = data.results || data.map(toModel); // Map the fields
          const promises = items.map((item: any) => {
            if (typeof item.user === 'number') {
              return this.$repositories.user.get(item.user)
                .then((userData: any) => {
                  item.user = userData;
                })
                .catch(() => {
                  item.user = { username: 'N/A' };
                });
            } else {
              return Promise.resolve();
            }
          });
          Promise.all(promises)
            .then(() => {
              console.log('Processed Items:', items); // Log the processed items
              this.items = items;
              this.total = data.count || items.length;
            });
        })
        .catch((error: any) => {
          console.error('Error fetching perspectives:', error.response || error.message);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    updateQuery() {
      this.fetchPerspectives();
    },
    // Use the timeAgo function for relative date formatting.
    timeAgo(dateStr: string): string {
      if (!dateStr) return 'N/A';
      const dateObj = new Date(dateStr);
      // LOG the raw date for debugging
      console.log('Converting date:', dateStr, '->', dateObj);
      const now = new Date();
      const diffMs = now.valueOf() - dateObj.valueOf();
      const diffSeconds = Math.floor(diffMs / 1000);
      if (diffSeconds < 0) return 'right now';
      if (diffSeconds < 60) return diffSeconds + ' seconds ago';
      const diffMinutes = Math.floor(diffSeconds / 60);
      if (diffMinutes < 60) return diffMinutes + ' minutes ago';
      const diffHours = Math.floor(diffMinutes / 60);
      if (diffHours < 24) return diffHours + ' hours ago';
      const diffDays = Math.floor(diffHours / 24);
      if (diffDays < 7) return diffDays + ' days ago';
      if (diffDays < 30) return diffDays + ' days ago';
      const diffMonths = Math.floor(diffDays / 30);
      if (diffMonths < 12) return diffMonths + ' months ago';
      const diffYears = Math.floor(diffMonths / 12);
      return diffYears + ' years ago';
    },
    formatTime(time: string): string {
      // For easier debugging, you can also format time here or inspect raw values.
      return this.timeAgo(time);
    },
    async submitPerspective() {
      const projectId = Number(this.$route.params.id);
      const userId = this.$store.state.auth.id;
      if (!userId) {
        console.error('User ID is missing. Ensure the user is logged in.');
        return;
      }
      if (!this.form.text || !this.form.category || !this.form.subject) {
        console.error('Form is invalid. Ensure all required fields are filled.');
        return;
      }
      const payload = {
        subject: this.form.subject,
        text: this.form.text,
        category: this.form.category,
        user: userId,
      };
      console.log('Submitting perspective payload:', payload);
      try {
        await this.$repositories.perspective.create(projectId, payload);
        this.$router.push(this.localePath(`/projects/${projectId}/perspectives`));
      } catch (error: any) {
        console.error('Error submitting perspective:', error);
      }
    }
  },
  watch: {
    options: {
      handler() {
        this.updateQuery();
      },
      deep: true
    },
    search() {
      this.options.page = 1;
      this.updateQuery();
    }
  },
  mounted() {
    this.fetchPerspectives();
  }
});
</script>

<style scoped>
</style>