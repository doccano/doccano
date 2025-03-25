<template>
  <v-card>
    <v-card-title v-if="isStaff">
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
    </v-card-title>
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
import { User } from '~/domain/models/user/user'

export default Vue.extend({
  components: {
    UserList,
    FormDelete
  },
  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      dialogDelete: false,
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
      this.$store.dispatch('notification/setNotification', {
        color: 'error',
        text: 'Failed to load users'
      })
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

    async remove() {
      try {
        for (const user of this.selected) {
          await this.$services.user.deleteUser(user.id)
        }
        this.$store.dispatch('notification/setNotification', {
          color: 'success',
          text: 'Users deleted successfully'
        })
        this.$fetch()
      } catch (e) {
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Failed to delete users'
        })
      } finally {
        this.dialogDelete = false
        this.selected = []
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
