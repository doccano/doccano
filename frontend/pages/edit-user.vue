<template>
    <v-app id="inspire">
      <v-main>
        <v-container fluid class="pa-4">
          <v-row align="center" justify="center" class="mt-5">
            <v-col cols="12" sm="10" md="8">
              <!-- Card for User List -->
              <v-card class="pa-0 overflow-hidden rounded-lg shadow-lg">
                <v-sheet color="primary" class="py-4 px-6 rounded-t-lg">
                  <div class="text-h5 font-weight-bold text-white">
                    Edit Users
                  </div>
                </v-sheet>
    
                <v-card-text class="pa-4">
                  <v-text-field
                    v-model="search"
                    :prepend-inner-icon="mdiMagnify"
                    label="Search"
                    single-line
                    hide-details
                    filled
                    class="mb-4"
                  />
                    
                  <v-data-table
                    :headers="headers"
                    :items="sortedUsers"
                    :items-per-page="options.itemsPerPage"
                    item-key="id"
                    :loading="isLoading"
                    :loading-text="'Loading users...'"
                    hide-default-footer
                  >
                    <template v-slot:[`item.username`]="{ item }">
                      <span>{{ item.username }}</span>
                    </template>
    
                    <template v-slot:[`item.email`]="{ item }">
                      <span>{{ item.email }}</span>
                    </template>
    
                    <template v-slot:[`item.role`]="{ item }">
                      <v-chip :color="item.role === 'admin' ? '#FF2F00' : '#1976D2'" outlined>
                        {{ item.role }}
                      </v-chip>
                    </template>
    
                    <template v-slot:[`item.actions`]="{ item }">
                      <v-btn
                        depressed
                        small
                        :color="canEdit(item) ? 'primary' : 'grey'"
                        :disabled="!canEdit(item)"
                      >
                        EDIT
                      </v-btn>
                    </template>
    
                    <!-- Footer (only custom pagination will appear) -->
                    <template #footer>
                      <v-row>
                        <v-col class="d-flex justify-end">
                          <v-pagination
                            v-model="options.page"
                            :length="Math.ceil(users.length / options.itemsPerPage)"
                            total-visible="7"
                          />
                        </v-col>
                      </v-row>
                    </template>
                  </v-data-table>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
    
  <script>
  import { mdiMagnify } from '@mdi/js'
    
  export default {
    data() {
      return {
        valid: false,
        users: [],
        selectedUser: null,
        name: '',
        email: '',
        role: '',
        showError: false,
        errorMessage: '',
        search: '',
        isLoading: false,
        // Pagination options
        options: {
          itemsPerPage: 5,
          page: 1
        },
        headers: [
          { text: 'Username', value: 'username' },
          { text: 'Email', value: 'email' },
          { text: 'Role', value: 'role' },
          { text: 'Actions', value: 'actions', sortable: false }
        ],
        mdiMagnify,
      
        currentUser: {
          id: 1,
          role: 'admin',
          username: 'admin'
        }
      }
    },
    computed: {
      sortedUsers() {
        const usersWithRole = this.users.map(user => ({
          ...user,
          role: user.role || ((user.is_staff || user.is_superuser) ? 'admin' : 'annotator')
        }))
    
        const filtered = usersWithRole.filter(user =>
          user.username.toLowerCase().includes(this.search.toLowerCase()) ||
          user.email.toLowerCase().includes(this.search.toLowerCase())
        )
        return filtered.sort((a, b) => a.id - b.id)
      }
    },
    async created() {
      await this.fetchUsers()
    },
    methods: {
      async fetchUsers() {
        this.isLoading = true
        try {
          const response = await this.$axios.get('/v1/users/')
          this.users = response.data
        } catch (error) {
          console.error('Error fetching users:', error)
        } finally {
          this.isLoading = false
        }
      },
      async submitForm() {
        if (!this.valid) {
          this.showError = true
          this.errorMessage = 'Please fill in all required fields correctly'
          return
        }
        try {
          const userData = {
            username: this.name,
            email: this.email,
            role: this.role
          }
          await this.$axios.put(`/api/users/${this.selectedUser}/`, userData)
          console.log('User updated successfully')
          this.showError = false
        } catch (error) {
          this.showError = true
          let errorDetail = ''
          if (error.response && error.response.data) {
            for (const [field, messages] of Object.entries(error.response.data)) {
              if (Array.isArray(messages)) {
                errorDetail += `<strong>${field}:</strong> ${messages.join(', ')}<br/>`
              } else {
                errorDetail += `<strong>${field}:</strong> ${messages}<br/>`
              }
            }
          } else {
            errorDetail = 'User update failed'
          }
          this.errorMessage = errorDetail
          console.error('Update error:', error.response && error.response.data)
        }
      },
      // Determines if the EDIT button should be enabled
      canEdit(user) {
        if (this.currentUser.role === 'admin') {
          // Admin can edit annotators only (non-admins)
          return user.role !== 'admin'
        } else {
          // Annotators can only edit their own record
          return user.id === this.currentUser.id
        }
      }
    }
  }
  </script>
    
  <style scoped>
  /* Card Styles */
  .v-card {
    background-color: #ffffff;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
    
  .v-list-item-title,
  .v-list-item-subtitle {
    font-size: 1rem;
  }
    
  .v-chip {
    font-size: 0.9rem;
  }
    
  .v-container {
    padding: 20px;
  }
    
  .v-data-table {
    margin-top: 20px;
  }
    
  .v-pagination {
    margin-top: 10px;
  }
  </style>