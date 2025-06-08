<template>
  <v-container>
    <v-card>
      <v-card-title class="headline">
        <v-btn icon @click.stop="goBack">
          <v-icon>{{ icons.mdiArrowLeft }}</v-icon>
        </v-btn>
        <span v-if="user">User Settings</span>
        <span v-else>Loading user profile...</span>
      </v-card-title>

      <v-card-text>
        <v-alert v-if="errorMessage" type="error" dismissible>
          {{ errorMessage }}
        </v-alert>
        <v-alert v-if="successMessage" type="success" dismissible>
          {{ successMessage }}
        </v-alert>

        <div v-if="user">
          <p>
            Username: {{ user.username }}
            <v-chip v-if="user.isStaff" color="amber" class="ml-2" x-small>Staff</v-chip>
            <v-chip v-if="user.isSuperUser" color="orange" class="ml-2" x-small>Admin</v-chip>
            <v-chip v-if="user.isActive" color="blue" class="ml-2" x-small>Active</v-chip>
            <v-chip v-else color="red" class="ml-2" x-small>Inactive</v-chip>
          </p>
          <p>Email: {{ user.email }}</p>
          <p>First name: {{ user.firstName }}</p>
          <p>Last name: {{ user.lastName }}</p>
          <p>Joined at: {{ new Date(user.dateJoined).toLocaleString() }}</p>
        </div>

        <v-divider class="mb-5" />

        <v-form v-if="user" ref="form" @submit.prevent="updateUser">
          <h2 class="mb-5">Edit User:</h2>

          <v-text-field v-model="editedUser.username" label="Username" required />
          <v-switch v-model="editedUser.isStaff" color="amber" label="Staff" />
          <v-switch v-model="editedUser.isSuperUser" color="orange" label="Administrator" />

          <v-card-actions>
            <v-btn color="error" @click="handleSingleDelete" :disabled="loading">Delete User</v-btn>
            <v-spacer />
            <v-btn color="primary" class="mr-4" type="submit" :loading="loading" :disabled="loading">
              Update Profile
            </v-btn>
          </v-card-actions>
        </v-form>

        <v-progress-circular v-else indeterminate color="primary" />
      </v-card-text>
    </v-card>

    <v-dialog v-model="confirmDelete" max-width="420">
      <v-card class="rounded-lg elevation-10">
        <!-- Cabeçalho azul com ícone -->
        <v-card-title class="white--text d-flex align-center" style="background-color: #1976d2;">
          <v-icon left class="mr-2">mdi-help-circle</v-icon>
          <span class="headline">Delete User</span>
        </v-card-title>

        <v-card-text class="pa-5 text-body-1 grey--text text--darken-3">
          Are you sure you want to delete this user? This action cannot be undone.
        </v-card-text>

        <v-card-actions class="px-5 pb-4">
          <v-spacer />
          <v-btn text @click="confirmDelete = false">Cancel</v-btn>
          <v-btn text class="red--text" @click="deleteUser" :loading="deleteLoading">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <!-- Modal de erro -->
    <error-dialog :visible="errorDialog" :message="errorDialogMessage" @close="errorDialog = false" />
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiArrowLeft } from '@mdi/js'
import ErrorDialog from '@/components/common/ErrorDialog.vue'
import { UserApplicationService } from '@/services/application/user/UserApplicationService'
import { APIUserRepository } from '@/repositories/user/apiUserRepository'
import { UserDetails } from '@/domain/models/user/user'

export default Vue.extend({
  components: {
    ErrorDialog
  },
  layout: 'projects',
  data() {
    return {
      user: null as UserDetails | null,
      editedUser: {
        username: '',
        isStaff: false,
        isSuperUser: false
      },
      loading: false,
      deleteLoading: false,
      confirmDelete: false,
      errorDialog: false,
      errorDialogMessage: '',
      errorMessage: '',
      successMessage: '',
      icons: {
        mdiArrowLeft
      }
    }
  },

  async created() {
    await this.fetchUser()
  },

  methods: {
    async fetchUser() {
      try {
        const id = parseInt(this.$route.params.id)
        const userService = new UserApplicationService(new APIUserRepository())
        this.user = await userService.getUser(id)
        this.editedUser = {
          username: this.user.username,
          isStaff: this.user.isStaff,
          isSuperUser: this.user.isSuperUser
        }
      } catch (error) {
        this.errorMessage = error.message
      }
    },

    async updateUser() {
      try {
        this.loading = true
        this.errorMessage = ''
        this.successMessage = ''

        const id = parseInt(this.$route.params.id)
        const userService = new UserApplicationService(new APIUserRepository())
        await userService.updateUser(id, {
          username: this.editedUser.username,
          is_staff: this.editedUser.isStaff,
          is_superuser: this.editedUser.isSuperUser
        })

        this.successMessage = 'User profile updated successfully'
        await this.fetchUser()
      } catch (error) {
        this.errorMessage = error.message
      } finally {
        this.loading = false
      }
    },

    handleSingleDelete() {
      if (this.user?.isSuperUser || this.user?.isStaff) {
        this.errorDialogMessage = `Cannot delete: ${this.user.username}. Admins and staff cannot be deleted.`
        this.errorDialog = true
        return
      }
      this.confirmDelete = true
    },

    async deleteUser() {
  try {
    this.deleteLoading = true
    this.errorMessage = ''

    const id = parseInt(this.$route.params.id)
    const userService = new UserApplicationService(new APIUserRepository())
    await userService.deleteUser(id)

    this.confirmDelete = false
    this.$router.push('/users')
  } catch (error) {
    if (
      error.message.includes('Failed to fetch') || // fetch padrão
      error.message.includes('Network Error') ||    // Axios/network
      error.message.includes('ECONNREFUSED') ||     // Node.js/axios backend offline
      error.message.includes('502') ||              // Bad Gateway (nginx etc.)
      error.message.includes('504') ||              // Gateway Timeout
      error.message.includes('Failed to delete user') // custom errors
    ) {
      this.errorDialogMessage =
        'Unable to delete user: database connection failed. Check if the server is up.'
    } else {
      this.errorDialogMessage = error.message
    }
    this.errorDialog = true
    this.confirmDelete = false
  } finally {
    this.deleteLoading = false
  }
},

    goBack() {
      this.$router.go(-1)
    }
  }
})
</script>
