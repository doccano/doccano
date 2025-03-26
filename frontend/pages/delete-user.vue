<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid class="pa-4">
        <v-row align="center" justify="center" class="mt-5">
          <v-col cols="12" sm="10" md="8">
            <v-card class="pa-0 overflow-hidden rounded-lg shadow-lg">
              <v-sheet color="primary" class="py-4 px-6 rounded-t-lg">
                <div class="text-h6 font-weight-medium" style="color: white">Delete Users</div>
              </v-sheet>
              <v-card-text class="pa-4">
                <v-alert v-if="errorMessage" type="error" dismissible class="mb-4">
                  {{ errorMessage }}
                </v-alert>

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
                  :items="pagedUsers"
                  :items-per-page="options.itemsPerPage"
                  item-key="id"
                  :loading="isLoading"
                  loading-text="Loading users..."
                  :item-class="getRowClass"
                  :options.sync="options"
                  :custom-sort="customSort"
                  hide-default-footer
                >
                  <template #[`item.id`]="{ item }">
                    <span v-if="!item._empty">{{ item.id }}</span>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template #[`item.username`]="{ item }">
                    <div v-if="!item._empty" class="d-flex align-center">
                      <span
                        class="status-circle"
                        :style="{ backgroundColor: getStatusColor(item) }"
                      ></span>
                      <span>{{ item.username }}</span>
                    </div>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template #[`item.email`]="{ item }">
                    <span v-if="!item._empty">{{ item.email }}</span>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template #[`item.role`]="{ item }">
                    <v-chip
                      v-if="!item._empty"
                      :color="
                        item.role === 'owner'
                          ? '#a8c400'
                          : item.role === 'admin'
                          ? '#FF2F00'
                          : 'primary'
                      "
                      outlined
                    >
                      {{ item.role.charAt(0).toUpperCase() + item.role.slice(1) }}
                    </v-chip>
                    <div v-else>&nbsp;</div>
                  </template>
                  <template #[`item.date_joined`]="{ item }">
                    <span v-if="!item._empty">{{ timeAgo(item.date_joined) }}</span>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template #[`item.last_seen`]="{ item }">
                    <span v-if="!item._empty">
                      {{
                        isCurrentUser(item)
                          ? 'Currently online'
                          : item.last_login
                          ? timeAgo(item.last_login)
                          : 'Never'
                      }}
                    </span>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template #[`item.actions`]="{ item }">
                    <v-btn
                      v-if="!item._empty"
                      icon
                      color="red"
                      :disabled="!canDelete(item)"
                      @click="openDelete(item)"
                    >
                      <v-icon>{{ mdiTrashCan }}</v-icon>
                    </v-btn>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template #footer>
                    <v-row align="center">
                      <v-col class="d-flex justify-start">
                        <v-btn color="primary" @click="$router.push('/list-user')">
                          <v-icon left>{{ mdiChevronLeft }}</v-icon>
                          Back
                        </v-btn>
                      </v-col>
                      <v-col class="d-flex justify-end">
                        <v-pagination
                          v-model="options.page"
                          :length="Math.ceil(sortedUsers.length / options.itemsPerPage)"
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
        <v-dialog v-model="deleteDialog" max-width="500px">
          <v-card>
            <v-sheet color="primary" class="py-4 px-6 rounded-t-lg">
              <div class="text-h6 font-weight-medium" style="color: white">
                Delete User: {{ deletingUser.username || 'User' }}
              </div>
            </v-sheet>
            <v-card-text class="pa-4">
              <v-alert v-if="deleteErrorMessage" type="error" dismissible class="mb-4">
                {{ deleteErrorMessage }}
              </v-alert>
              <div v-if="deletingUser && deletingUser.id && deletingUser.id === currentUserId">
                Are you sure you want to delete your own account?
              </div>
              <div v-else-if="deletingUser && deletingUser.username">
                Are you sure you want to delete user
                <strong>{{ deletingUser.username }}</strong
                >?
              </div>
              <div v-else>Are you sure you want to delete this user?</div>
            </v-card-text>
            <v-card-actions>
              <v-btn color="red" class="white--text" @click="deleteUser">Delete</v-btn>
              <v-btn text @click="closeDelete">Cancel</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mdiMagnify, mdiChevronLeft, mdiTrashCan } from '@mdi/js'
import { mapState } from 'vuex'

export default {
  data() {
    return {
      users: [],
      search: '',
      isLoading: false,
      errorMessage: '',
      deleteErrorMessage: '',
      options: {
        itemsPerPage: 5,
        page: 1,
        sortBy: [],
        sortDesc: []
      },
      mdiChevronLeft,
      mdiTrashCan,
      headers: [
        { text: 'Username', value: 'username', sortable: true },
        { text: 'Email', value: 'email', sortable: true },
        { text: 'Role', value: 'role', sortable: true },
        { text: 'Joined', value: 'date_joined', sortable: true },
        { text: 'Last Seen', value: 'last_seen', sortable: true },
        { text: 'Actions', value: 'actions', sortable: false }
      ],
      mdiMagnify,
      deleteDialog: false,
      deletingUser: {}
    }
  },
  computed: {
    ...mapState('auth', {
      id: (state) => state.id,
      isStaff: (state) => state.isStaff,
      is_superuser: (state) => state.is_superuser
    }),
    currentUser() {
      return {
        id: this.id,
        role:
          this.is_superuser && this.isStaff
            ? 'owner'
            : !this.is_superuser && this.isStaff
            ? 'admin'
            : 'annotator'
      }
    },
    currentUserId() {
      return this.currentUser.id
    },
    currentUserRole() {
      return this.currentUser.role
    },
    sortedUsers() {
      const lowerSearch = this.search.toLowerCase()
      const usersWithRole = this.users.map((user) => ({
        ...user,
        role: user.role
          ? user.role
          : user.is_staff && !user.is_superuser
          ? 'admin'
          : user.is_superuser && user.is_staff
          ? 'owner'
          : 'annotator'
      }))
      const filtered = usersWithRole.filter(
        (user) =>
          user.username.toLowerCase().includes(lowerSearch) ||
          user.email.toLowerCase().includes(lowerSearch)
      )
      return this.customSort(filtered, this.options.sortBy, this.options.sortDesc)
    },
    pagedUsers() {
      const start = (this.options.page - 1) * this.options.itemsPerPage
      const end = start + this.options.itemsPerPage
      const pageItems = this.sortedUsers.slice(start, end)
      while (pageItems.length < this.options.itemsPerPage) {
        pageItems.push({ _empty: true })
      }
      return pageItems
    },
    roleOptions() {
      const options = [
        { text: 'Annotator', value: 'annotator', disabled: false },
        { text: 'Admin', value: 'admin', disabled: false },
        { text: 'Owner', value: 'owner', disabled: false }
      ]
      const deletingSelf = this.deletingUser && this.deletingUser.id === this.currentUserId
      if (!deletingSelf) {
        if (this.currentUserRole === 'annotator') {
          options.find((opt) => opt.value === 'admin').disabled = true
          options.find((opt) => opt.value === 'owner').disabled = true
        } else if (this.currentUserRole === 'admin') {
          options.find((opt) => opt.value === 'owner').disabled = true
        }
      }
      return options
    }
  },
  watch: {
    search() {
      this.options.page = 1
      this.fetchUsers()
    }
  },
  async created() {
    await this.fetchUsers()
    console.log(this.$store.state.auth)
  },
  methods: {
    async fetchUsers() {
      this.isLoading = true
      try {
        const response = await this.$axios.get('/v1/users/')
        this.users = response.data
        this.errorMessage = ''
      } catch (error) {
        if (error.response && error.response.data) {
          const data = error.response.data
          if (typeof data === 'string' && data.trim().startsWith('<')) {
            this.errorMessage = "Error: Can't access our database!"
          } else {
            const errors = []
            for (const [field, messages] of Object.entries(data)) {
              const formattedMessages = Array.isArray(messages) ? messages.join(', ') : messages
              errors.push(
                `${field.charAt(0).toUpperCase() + field.slice(1)}: ${formattedMessages.replace(
                  /^\n+/,
                  ''
                )}`
              )
            }
            this.errorMessage = errors.join('\n\n')
          }
        } else {
          this.errorMessage = 'Error fetching users'
        }
        console.error('Error fetching users:', error)
      } finally {
        this.isLoading = false
      }
    },
    getRowClass(item) {
      return item._empty ? 'dummy-row' : ''
    },
    canDelete(user) {
      if (user.id === this.currentUserId) return true
      if (this.currentUserRole === 'owner') {
        return user.role !== 'owner'
      }
      if (this.currentUserRole === 'admin') {
        return user.role === 'annotator'
      }
      return false
    },
    openDelete(item) {
      this.deletingUser = { ...item }
      this.deleteDialog = true
    },
    async deleteUser() {
      try {
        // Clear any previous deletion errors
        this.deleteErrorMessage = ''
        await this.$axios.delete(`/v1/users/${this.deletingUser.id}/`)
        if (this.deletingUser.id === this.currentUserId) {
          this.deleteDialog = false
          this.$router.push({
            path: '/message',
            query: { message: 'Your account has been deleted!', redirect: '/home' }
          })
          setTimeout(() => {
            this.$store.dispatch('auth/logout')
          }, 500)
        } else {
          this.users = this.users.filter((u) => u.id !== this.deletingUser.id)
          this.deleteDialog = false
          this.$router.push({
            path: '/message',
            query: { message: 'User deleted successfully!', redirect: '/delete-user' }
          })
        }
      } catch (error) {
        console.error('Error deleting user:', error)
        this.deleteErrorMessage = "Error: Can't access our database!"
      }
    },
    closeDelete() {
      this.deleteDialog = false
      this.deleteErrorMessage = ''
    },
    isCurrentUser(user) {
      return user.id === this.currentUserId
    },
    getStatusColor(user) {
      return this.isCurrentUser(user) ? 'green' : 'red'
    },
    timeAgo(dateStr) {
      if (!dateStr) return ''
      const now = new Date()
      const past = new Date(dateStr)
      const diffMs = now - past
      const diffSeconds = Math.floor(diffMs / 1000)
      if (diffSeconds < 0) return 'right now'
      if (diffSeconds < 60) return diffSeconds + ' seconds ago'
      const diffMinutes = Math.floor(diffSeconds / 60)
      if (diffMinutes < 60) return diffMinutes + ' minutes ago'
      const diffHours = Math.floor(diffMinutes / 60)
      if (diffHours < 24) return diffHours + ' hours ago'
      const diffDays = Math.floor(diffHours / 24)
      if (diffDays < 7) return diffDays + ' days ago'
      if (diffDays < 30) return diffDays + ' days ago'
      const diffMonths = Math.floor(diffDays / 30)
      if (diffMonths < 12) return diffMonths + ' months ago'
      const diffYears = Math.floor(diffMonths / 12)
      return diffYears + ' years ago'
    },
    customSort(items, sortBy, sortDesc) {
      if (!sortBy.length) {
        return items.sort((a, b) => {
          if (a._empty && !b._empty) return 1
          if (!a._empty && b._empty) return -1
          return (a.id || 0) - (b.id || 0)
        })
      }
      const field = sortBy[0]
      return items.sort((a, b) => {
        if (a._empty && !b._empty) return 1
        if (!a._empty && b._empty) return -1
        if (a._empty && b._empty) return 0
        let comp = 0
        if (field === 'role') {
          const order = { annotator: 0, admin: 1, owner: 2 }
          comp = order[a.role] - order[b.role]
        } else if (field === 'date_joined') {
          comp = new Date(a.date_joined) - new Date(b.date_joined)
        } else if (field === 'last_seen') {
          comp = new Date(a.last_login) - new Date(b.last_login)
        } else if (field === 'id') {
          comp = (a.id || 0) - (b.id || 0)
        } else if (typeof a[field] === 'string') {
          comp = a[field].localeCompare(b[field])
        } else {
          comp = (a[field] || 0) - (b[field] || 0)
        }
        return sortDesc[0] ? -comp : comp
      })
    }
  }
}
</script>

<style scoped>
.v-card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
::v-deep tr.dummy-row:hover {
  background-color: transparent !important;
}
.status-circle {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
  position: relative;
}
.theme--dark .v-card {
  background-color: #1e1e1e !important;
  color: #ffffff;
}

.theme--dark .v-text-field input {
  color: #ffffff;
}

.theme--dark .v-select .v-input__slot {
  background-color: #0f0f0f !important;
  color: #ffffff;
}

.theme--dark .v-text-field {
  background-color: #0f0f0f !important;
  color: #ffffff;
}

.theme--dark .v-text-field :hover {
  background-color: #191919 !important;
  color: #ffffff;
}

.theme--dark .v-text-field input {
  color: #ffffff;
}

:deep(.theme--dark .v-data-table tbody tr:hover:not(.dummy-row)) {
  background-color: #151515 !important;
}
</style>
