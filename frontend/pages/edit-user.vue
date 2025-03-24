<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid class="pa-4">
        <!-- Main Card -->
        <v-row align="center" justify="center" class="mt-5">
          <v-col cols="12" sm="10" md="8">
            <v-card class="pa-0 overflow-hidden rounded-lg shadow-lg">
              <v-sheet color="primary" class="py-4 px-6 rounded-t-lg">
                <div class="text-h6 font-weight-medium text--white">
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
                  <template v-slot:[`item.id`]="{ item }">
                    <span v-if="!item._empty">{{ item.id }}</span>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template v-slot:[`item.username`]="{ item }">
                    <div v-if="!item._empty" class="d-flex align-center">
                      <span class="status-circle" :style="{ 
                        backgroundColor: getStatusColor(item) 
                        }"></span>
                      <span>{{ item.username }}</span>
                    </div>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template v-slot:[`item.email`]="{ item }">
                    <span v-if="!item._empty">{{ item.email }}</span>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template v-slot:[`item.role`]="{ item }">
                    <v-chip
                      v-if="!item._empty"
                      :color="item.role === 'owner' ? '#a8c400' : 
                      (item.role === 'admin' ? 
                      '#FF2F00' : 'primary')"
                      outlined
                    >
                      {{ item.role.charAt(0).toUpperCase() + item.role.slice(1) }}
                    </v-chip>
                    <div v-else>&nbsp;</div>
                  </template>
                  <template v-slot:[`item.date_joined`]="{ item }">
                    <span v-if="!item._empty">{{ timeAgo(item.date_joined) }}</span>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template v-slot:[`item.last_seen`]="{ item }">
                    <span v-if="!item._empty">
                      {{ isCurrentUser(item) ? 'Currently online' 
                      : (item.last_login 
                      ? timeAgo(item.last_login) 
                      : 'Never') }}
                    </span>
                    <span v-else>&nbsp;</span>
                  </template>
                  <template v-slot:[`item.actions`]="{ item }">
                    <v-btn
                      v-if="!item._empty"
                      color="primary"
                      small
                      :disabled="!canEdit(item)"
                      @click="openEdit(item)"
                    >
                      EDIT
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
        <!-- Edit User Dialog -->
        <v-dialog v-model="editDialog" max-width="500px">
          <v-card>
            <v-sheet color="primary" class="py-4 px-6 rounded-t-lg">
              <div class="text-h6 font-weight-medium text--white">
                Edit User: {{ editingUser.username || 'New User' }}
              </div>
            </v-sheet>
            <v-card-text class="pa-4">
              <v-form ref="editForm">
                <v-text-field
                  v-model="editingUser.username"
                  label="Username"
                  outlined
                ></v-text-field>
                <v-text-field
                  v-model="editingUser.email"
                  label="Email"
                  outlined
                ></v-text-field>
                <v-select
                  v-model="editingUser.role"
                  :items="roleOptions"
                  label="Role"
                  outlined
                ></v-select>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" @click="saveEdit">Save</v-btn>
              <v-btn text @click="closeEdit">Cancel</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-container>
    </v-main>
  </v-app>
</template>
  
<script>
import { mdiMagnify } from '@mdi/js'
import { mdiChevronLeft } from '@mdi/js'
import { mapState } from 'vuex'
  
export default {
  data() {
    return {
      users: [],
      search: '',
      isLoading: false,
      options: {
        itemsPerPage: 5,
        page: 1,
        sortBy: [],
        sortDesc: []
      },
      mdiChevronLeft,
      headers: [
        { text: 'Username', value: 'username', sortable: true },
        { text: 'Email', value: 'email', sortable: true },
        { text: 'Role', value: 'role', sortable: true },
        { text: 'Joined', value: 'date_joined', sortable: true },
        { text: 'Last Seen', value: 'last_seen', sortable: true },
        { text: 'Actions', value: 'actions', sortable: false }
      ],
      mdiMagnify,
      editDialog: false,
      editingUser: {}
    }
  },
  computed: {
    ...mapState('auth', {
      id: state => state.id,
      isStaff: state => state.isStaff,
      is_superuser: state => state.is_superuser
    }),
    currentUser() {
      return {
        id: this.id,
        role: (this.is_superuser && this.isStaff)
          ? 'owner'
          : (!this.is_superuser && this.isStaff)
          ? 'admin'
          : 'annotator'
      }
    },
    currentUserId() {
      return this.currentUser.id;
    },
    currentUserRole() {
      return this.currentUser.role;
    },
    roleOptions() {
      const options = [
        { text: 'Annotator', value: 'annotator' },
        { text: 'Admin', value: 'admin' }
      ];
      if (this.currentUserRole === 'owner') {
        options.push({ text: 'Owner', value: 'owner' });
      }
      return options;
    },
    sortedUsers() {
      const lowerSearch = this.search.toLowerCase();
      const usersWithRole = this.users.map(user => ({
        ...user,
        role: user.role 
          ? user.role 
          : (user.is_staff && !user.is_superuser ? 'admin' 
            : (user.is_superuser && user.is_staff ? 'owner' : 'annotator'))
      }));
      // Use the search term in filtering so it always re-computes
      const filtered = usersWithRole.filter(user =>
        user.username.toLowerCase().includes(lowerSearch) ||
        user.email.toLowerCase().includes(lowerSearch)
      );
      return this.customSort(filtered, this.options.sortBy, this.options.sortDesc);
    },
    pagedUsers() {
      const start = (this.options.page - 1) * this.options.itemsPerPage;
      const end = start + this.options.itemsPerPage;
      const pageItems = this.sortedUsers.slice(start, end);
      while (pageItems.length < this.options.itemsPerPage) {
        pageItems.push({ _empty: true });
      }
      return pageItems;
    }
  },
  async created() {
    await this.fetchUsers();
    console.log(this.$store.state.auth);
  },
  methods: {
    async fetchUsers() {
      this.isLoading = true;
      try {
        const response = await this.$axios.get('/v1/users/');
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      } finally {
        this.isLoading = false;
      }
    },
    getRowClass(item) {
      return item._empty ? 'dummy-row' : '';
    },
    canEdit(user) {
      // Allow self-edit
      if (user.id === this.currentUserId) return true;
      
      // Owners can edit anyone except other owners
      if (this.currentUserRole === 'owner') {
        return user.role !== 'owner';
      }
      
      // Admins can only edit annotators
      if (this.currentUserRole === 'admin') {
        return user.role === 'annotator';
      }
      
      return false;
    },
    openEdit(item) {
      this.editingUser = { ...item };
      this.editDialog = true;
    },
    async saveEdit() {
      try {
        if (this.editingUser.role === 'owner' && this.currentUserRole !== 'owner') {
          alert("Only an owner can assign the Owner role.");
          return;
        }
        if (this.editingUser.role === 'owner') {
          this.editingUser.is_superuser = true;
          this.editingUser.is_staff = true;
          // role remains 'owner'
        } else if (this.editingUser.role === 'admin') {
          // Allow assignment if current user is admin or owner
          if (this.currentUserRole === 'annotator') {
            // annotators can only assign annotator
            this.editingUser.is_superuser = false;
            this.editingUser.is_staff = false;
            this.editingUser.role = 'annotator';
          } else {
            // currentUser is admin or owner, so allow upgrading to admin
            this.editingUser.is_superuser = false;
            this.editingUser.is_staff = true;
            this.editingUser.role = 'admin';
          }
        } else {
          // Assign annotator
          this.editingUser.is_superuser = false;
          this.editingUser.is_staff = false;
          this.editingUser.role = 'annotator';
        }
        let response;
        if (this.editingUser.id) {
          response = await this.$axios.put(`/v1/users/${this.editingUser.id}/`, this.editingUser);
          const index = this.users.findIndex(u => u.id === this.editingUser.id);
          if (index !== -1) {
            this.$set(this.users, index, response.data);
          }
        } else {
          response = await this.$axios.post('/v1/users/', this.editingUser);
          this.users.push(response.data);
        }
        // Reset to first page so search filtering works correctly
        this.options.page = 1;
        // Optionally, re-fetch users to ensure reactive data:
        // await this.fetchUsers();
        this.editDialog = false;
      } catch (error) {
        console.error('Error saving user:', error);
      }
    },
    closeEdit() {
      this.editDialog = false;
    },
    isCurrentUser(user) {
      return user.id === this.currentUserId;
    },
    getStatusColor(user) {
      return this.isCurrentUser(user) ? 'green' : 'red';
    },
    timeAgo(dateStr) {
      if (!dateStr) return '';
      const now = new Date();
      const past = new Date(dateStr);
      const diffMs = now - past;
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
    customSort(items, sortBy, sortDesc) {
      if (!sortBy.length) {
        return items.sort((a, b) => {
          if (a._empty && !b._empty) return 1;
          if (!a._empty && b._empty) return -1;
          return (a.id || 0) - (b.id || 0);
        });
      }
      const field = sortBy[0];
      return items.sort((a, b) => {
        if (a._empty && !b._empty) return 1;
        if (!a._empty && b._empty) return -1;
        if (a._empty && b._empty) return 0;
        let comp = 0;
        if (field === 'role') {
          const order = { annotator: 0, admin: 1, owner: 2 };
          comp = order[a.role] - order[b.role];
        } else if (field === 'date_joined') {
          comp = new Date(a.date_joined) - new Date(b.date_joined);
        } else if (field === 'last_seen') {
          comp = new Date(a.last_login) - new Date(b.last_login);
        } else if (field === 'id') {
          comp = (a.id || 0) - (b.id || 0);
        } else if (typeof a[field] === 'string') {
          comp = a[field].localeCompare(b[field]);
        } else {
          comp = (a[field] || 0) - (b[field] || 0);
        }
        return sortDesc[0] ? -comp : comp;
      });
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
  z-index: 1;
}
</style>