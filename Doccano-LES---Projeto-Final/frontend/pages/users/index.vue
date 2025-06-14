<template>
  <v-card>
    <v-card-title>
      <v-btn class="text-capitalize" color="primary" @click.stop="$router.push('users/add')">
        {{ $t('generic.create') }}
      </v-btn>
      <v-btn
        class="text-capitalize ms-2"
        outlined
        :disabled="!canDelete"
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @remove="handleDelete" @cancel="dialogDelete = false" />
      </v-dialog>
      <v-dialog v-model="dialogEdit">
        <form-edit :user="selected[0]" @confirmEdit="handleEdit" @cancel="dialogEdit = false" />
      </v-dialog>
    </v-card-title>
    <user-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
      @editUser="openEditDialog"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import FormDelete from '@/components/user/FormDelete.vue'
import UserList from '@/components/user/UserList.vue'
import { UserDTO } from '~/services/application/user/userData'
import FormEdit from '@/components/user/FormEdit.vue'

export default Vue.extend({
  components: {
    FormDelete,
    FormEdit,
    UserList
  },

  layout: 'projects',

  middleware: ['check-auth', 'auth', 'isSuperUser'],

  data() {
    return {
      dialogDelete: false,
      items: [] as UserDTO[],
      selected: [] as UserDTO[],
      dialogEdit: false,
      isLoading: false,
      tab: 0,
      drawerLeft: null
    }
  },

  computed: {
    ...mapGetters('auth', ['isStaff', 'isSuperUser']),

    canDelete(): boolean {
      return this.selected.length > 0
    }
  },

  mounted() {
    this.fetchUsers()
  },

  methods: {
    async fetchUsers() {
      this.isLoading = true
      try {
        const response = await this.$services.user.list()
        this.items = response
      } catch (error) {
        console.error('Erro ao buscar utilizadores:', error)
      } finally {
        this.isLoading = false
      }
    },
    async deleteUser(userId: number) {
      this.isLoading = true
      try {
        await this.$services.user.delete(userId)
        this.items = this.items.filter((user) => user.id !== userId)
      } catch (error) {
        console.error('Erro ao excluir utilizador:', error)
      } finally {
        this.isLoading = false
      }
    },
    async handleDelete() {
      this.isLoading = true
      try {
        // Tries to delete each selected user
        for (const user of this.selected) {
          await this.$services.user.delete(user.id)
        }
        // Updates the list by removing the deleted users
        this.items = this.items.filter(
          (user) => !this.selected.some((selectedUser) => selectedUser.id === user.id)
        )
        this.selected = []
        this.dialogDelete = false // Closes the dialog on success

        // Shows an alert when the users are successfully removed with a delay
        setTimeout(() => {
          alert('Users successfully removed!')
        }, 180)
      } catch (error) {
        this.dialogDelete = false

        setTimeout(() => {
          console.error('Error deleting users:', error)
          const err = error as any

          // Check if the error is about deleting the own account
          if (err.response && err.response.status === 403) {
            alert('You cannot delete your own account.')
          }
          // General error alert for other cases
          else {
            alert('Error: The database is currently unavailable. Please try again later.')
          }
        }, 180)
      } finally {
        this.isLoading = false
      }
    },
    async handleEdit(updatedUser: UserDTO) {
      this.isLoading = true
      try {
        await this.$services.user.update(updatedUser.id, updatedUser)

        // Atualiza localmente a lista com os dados editados
        this.items = this.items.map((user) => (user.id === updatedUser.id ? updatedUser : user))

        this.dialogEdit = false
        this.selected = []
      } catch (error) {
        console.error('Erro ao editar utilizador:', error)

        const err = error as any
        if (err.response && err.response.status >= 500) {
          alert('A base de dados está desligada, tente mais tarde!')
        } else {
          alert('Erro ao editar utilizador.')
        }
      } finally {
        this.isLoading = false
      }
    },
    openEditDialog(user: UserDTO) {
      this.selected = [user]
      this.dialogEdit = true
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
