<template>
  <v-card>
    <v-card-title>
      <v-btn class="text-capitalize" color="primary" @click.stop="dialogCreate = true">
        {{ $t('generic.create') }}
      </v-btn>
    </v-card-title>
    <users-list
      v-model="selected"
      :items="users.items"
      :is-loading="isLoading"
      :total="users.count"
      @update:query="updateQuery"
    />
    <v-dialog v-model="dialogCreate">
      <form-create @created="handleUserCreated" />
    </v-dialog>
  </v-card>
</template>

<script lang="ts">
import _ from 'lodash'
import Vue from 'vue'
import FormCreate from '@/components/users/FormCreate.vue'
import UsersList from '@/components/users/UsersList.vue'
import { Page } from '~/domain/models/page'
import { User } from '~/domain/models/user'

export default Vue.extend({
  components: {
    FormCreate,
    UsersList
  },

  layout: 'settings',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      users: {} as Page<User>,
      selected: [] as User[],
      isLoading: false,
      dialogCreate: false
    }
  },

  async fetch() {
    await this.fetchUsers()
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  methods: {
    async fetchUsers() {
      this.isLoading = true
      this.users = await this.$services.user.list(this.$route.query)
      this.isLoading = false
    },

    updateQuery(query: object) {
      this.$router.push({ query })
    },

    handleUserCreated() {
      this.dialogCreate = false
      this.fetchUsers()
    }
  }
})
</script>