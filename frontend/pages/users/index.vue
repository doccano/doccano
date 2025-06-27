<template>
  <v-card>
    <!-- Título com botão "Delete" -->
    <v-card-title v-if="isStaff">
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="beforeOpenDeleteDialog"
      >
        {{ $t('generic.delete') }}
      </v-btn>
    </v-card-title>

    <!-- Modal de confirmação de exclusão -->
    <v-dialog v-model="dialogDelete" max-width="500" scrollable>

      <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
    </v-dialog>

    <!-- Modal de erro -->
    <error-dialog
      :visible="errorDialog"
      :message="errorMessage"
      @close="errorDialog = false"
    />

    <!-- Lista de usuários -->
    <user-list
      v-model="selected"
      :items="users"
      :is-loading="isLoading"
      :total="total"
      @update:query="updateQuery"
    />
  </v-card>
</template>

<script lang="ts">
import _ from 'lodash'
import Vue from 'vue'
import { mapGetters } from 'vuex'
import UserList from '@/components/user/UserList.vue'
import FormDelete from '~/components/user/FormDelete.vue'
import ErrorDialog from '@/components/common/ErrorDialog.vue'
import { User } from '~/domain/models/user/user'

export default Vue.extend({
  components: {
    UserList,
    FormDelete,
    ErrorDialog
  },
  layout: 'projects',
  middleware: ['check-auth', 'auth'],

  data() {
    return {
      dialogDelete: false,
      errorDialog: false,
      errorMessage: '',
      users: [] as User[],
      selected: [] as User[],
      isLoading: false,
      total: 0
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      const query = this.buildQuery()
      const list = await this.$services.user.list(query)
      this.users = list.results
      this.total = list.count
    } catch (e) {
      this.errorMessage = 'Failed to load users'
      this.errorDialog = true
    } finally {
      this.isLoading = false
    }
  },

  computed: {
    ...mapGetters('auth', ['isStaff']),
    canDelete(): boolean {
      return this.selected.length > 0
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  methods: {
    buildQuery() {
      const { q, limit, offset, ordering, orderBy } = this.$route.query
      let query = ''
      if (q && q.length) query += `q=${q}&`
      if (offset) query += `offset=${offset}&`
      if (limit) query += `limit=${limit}&`
      if (ordering) query += `ordering=${orderBy}${ordering}&`
      return query
    },

    beforeOpenDeleteDialog() {
      const blockedUsers = this.selected.filter(user => user.isSuperUser || user.isStaff)
      if (blockedUsers.length > 0) {
        const names = blockedUsers.map(u => u.username).join(', ')
        this.errorMessage = `Cannot delete: ${names}. Admins and staff cannot be deleted.`
        this.errorDialog = true
        return
      }
      this.dialogDelete = true
    },

    async remove() {
  try {
    for (const user of this.selected) {
      try {
        await this.$services.user.deleteUser(user.id)
      } catch (error) {
        throw new Error('network-failure')  // personaliza o erro para tratar abaixo
      }
    }
    this.dialogDelete = false
    this.selected = []
    this.$fetch()
  } catch (e) {
    this.dialogDelete = false
    const message = String(e.message || e)
    if (message === 'network-failure') {
      this.errorMessage =
        'Unable to delete user: database connection failed. Check if the server is up.'
    } else {
      this.errorMessage = message
    }
    this.errorDialog = true
  }
},

    updateQuery(query: object) {
      this.$router.push(query)
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
