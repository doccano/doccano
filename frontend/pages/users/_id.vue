<template>
  <v-container>
    <v-card>
      <v-card-title class="headline">
        <v-btn icon
        @click.stop="goBack">
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
            <p>Username: {{ user.username }}
                <v-chip
                  v-if="user.isStaff"
                  color="amber"
                  class="ml-2"
                  x-small
                >
                  Staff
                </v-chip>
                <v-chip
                  v-if="user.isSuperuser"
                  color="orange"
                  class="ml-2"
                  x-small
                >
                  Admin
                </v-chip>
                <v-chip
                  v-if="user.isActive"
                  color="blue"
                  class="ml-2"
                  x-small
                >
                    Active
                </v-chip>
                <v-chip
                  v-else
                  color="red"
                  class="ml-2"
                  x-small
                >
                    Inactive
                </v-chip>
            </p>
            <p>
                Email: {{ user.email }}
            </p>
            <p>Fist name: {{ user.firstName }}</p>
            <p>Last name: {{ user.lastName }}</p>
            <p>Joined at: {{ user.dateJoined }}</p>
        </div>
        <v-divider class="mb-5"></v-divider>
        <v-form v-if="user" ref="form" @submit.prevent="updateUser">
        <h2 class="mb-5">Edit User:</h2>
          <v-text-field
            v-model="editedUser.username"
            label="Username"
            required
          ></v-text-field>
          <v-switch
            v-model="editedUser.isStaff"
            color="amber"
            label="Staff"
            hint="User has staff privileges"
          ></v-switch>
          <v-switch
            v-model="editedUser.isSuperuser"
            color="orange"
            label="Administrator"
            hint="User has administrative privileges"
          ></v-switch>
          <v-card-actions>
            <v-btn
              color="error"
              @click="confirmDelete = true"
              :disabled="loading"
            >
              Delete User
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              class="mr-4"
              type="submit"
              :loading="loading"
              :disabled="loading"
            >
              Update Profile
            </v-btn>
          </v-card-actions>
        </v-form>
        <v-progress-circular v-else indeterminate color="primary"></v-progress-circular>
      </v-card-text>
    </v-card>

    <v-dialog v-model="confirmDelete" max-width="400">
      <v-card>
        <v-card-title>Delete User</v-card-title>
        <v-card-text>
          Are you sure you want to delete this user? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="confirmDelete = false">Cancel</v-btn>
          <v-btn color="error" text @click="deleteUser" :loading="deleteLoading">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiArrowLeft } from '@mdi/js'
import { UserApplicationService } from '@/services/application/user/UserApplicationService'
import { APIUserRepository } from '@/repositories/user/apiUserRepository'
import { UserDetails } from '@/domain/models/user/user'

export default Vue.extend({
    layout: 'projects',
  data() {
    return {
      user: null as UserDetails | null,
      editedUser: {
        username: '',
        isStaff: false,
        isSuperuser: false
      },
      loading: false,
      deleteLoading: false,
      confirmDelete: false,
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
          isSuperuser: this.user.isSuperuser
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
          is_superuser: this.editedUser.isSuperuser
        })
        
        this.successMessage = 'User profile updated successfully'
        await this.fetchUser()
      } catch (error) {
        this.errorMessage = error.message
      } finally {
        this.loading = false
      }
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
        this.errorMessage = error.message
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
