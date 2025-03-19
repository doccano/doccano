<template>
  <v-card>
      <!-- Data Table with Search Bar -->
      <v-data-table
        :headers="headers"
        :items="users"
        :options.sync="options"
        :server-items-length="total"
        :search="searchQuery"
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
      >
        <!-- Search Bar -->
        <template #top>
          <v-text-field
            v-model="searchQuery"
            :prepend-inner-icon="mdiMagnify"
            :label="$t('generic.search')"
            single-line
            hide-details
            filled
          />
        </template>
        <!-- Custom Column Templates -->
        <template #[`item.username`]="{ item }">
          <nuxt-link :to="`/users/${item.id}`">
            <span>{{ item.username }}</span>
          </nuxt-link>
        </template>

        <template #[`item.email`]="{ item }">
          <span>{{ item.email }}</span>
        </template>
      </v-data-table>
      
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue';
import { mdiMagnify } from '@mdi/js';
import { APIUserRepository } from '@/repositories/user/apiUserRepository';
import { UserItem } from '@/domain/models/user/user';

export default Vue.extend({
  layout: 'users',
  middleware: ['check-auth', 'auth'],
  data() {
    return {
      users: [] as UserItem[],
      searchQuery: '',
      isLoading: false,
      total: 0,
      options: {} as any,
      mdiMagnify,
    };
  },

  computed: {
    headers(): { text: string; value: string; sortable?: boolean }[] {
      return [
        { text: 'Username', value: 'username' },
        { text: 'Email', value: 'email' },
        { text: 'Actions', value: 'actions', sortable: false },
      ];
    },
  },

  watch: {
    options: {
      handler() {
        this.fetchUsers();
      },
      deep: true,
    },
    searchQuery() {
      this.fetchUsers();
    },
  },

  async created() {
    await this.fetchUsers();
  },

  methods: {
    async fetchUsers() {
      this.isLoading = true;
      try {
        const userRepository = new APIUserRepository();
        const response = await userRepository.list(this.searchQuery);
        this.users = response;
        this.total = response.length;
      } catch (error) {
        console.error('Error fetching users:', error);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>