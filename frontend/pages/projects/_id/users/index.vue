<template>
  <v-content>
    <v-container
      fluid
      fill-height
    >
      <v-layout
        justify-center
      >
        <v-flex>
          <v-card>
            <v-card-title>
              <v-btn
                class="mb-2 text-capitalize"
                color="primary"
                @click="openAddModal"
              >
                Add User
              </v-btn>
              <Modal
                ref="childDialogue"
                :title="addModal.title"
                :button="addModal.button"
              >
                <v-autocomplete
                  v-model="selectedUser"
                  :items="items"
                  :loading="isLoading"
                  :search-input.sync="username"
                  color="white"
                  hide-no-data
                  hide-selected
                  item-text="username"
                  label="User Search APIs"
                  placeholder="Start typing to Search"
                  prepend-icon="mdi-account"
                  return-object
                />
                <v-select
                  :items="roles"
                  label="Role"
                  prepend-icon="mdi-account-card-details-outline"
                />
              </Modal>
              <v-btn
                class="mb-2 ml-2 text-capitalize"
                outlined
                :disabled="selected.length === 0"
                @click="openRemoveModal"
              >
                Remove
              </v-btn>
              <Modal
                ref="removeDialogue"
                :title="removeModal.title"
                :button="removeModal.button"
              >
                Are you sure you want to remove these users from this project?
                <v-list dense>
                  <v-list-item v-for="(user, i) in selected" :key="i">
                    <v-list-item-content>
                      <v-list-item-title>{{ user.name }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </Modal>
            </v-card-title>
            <v-data-table
              v-model="selected"
              :headers="headers"
              :items="users"
              item-key="name"
              :search="search"
              show-select
            >
              <template v-slot:top>
                <v-text-field
                  v-model="search"
                  prepend-inner-icon="search"
                  label="Search"
                  single-line
                  hide-details
                  filled
                />
              </template>
              <template v-slot:item.role="props">
                <v-edit-dialog
                  :return-value.sync="props.item.role"
                  large
                  persistent
                  @save="save"
                >
                  <div>{{ props.item.role }}</div>
                  <template v-slot:input>
                    <div class="mt-4 title">
                      Update Role
                    </div>
                  </template>
                  <template v-slot:input>
                    <v-select
                      v-model="props.item.role"
                      :items="roles"
                      label="Role"
                    />
                  </template>
                </v-edit-dialog>
              </template>
            </v-data-table>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import Modal from '~/components/Modal'

export default {
  layout: 'project',
  components: {
    Modal
  },
  data: () => ({
    search: '',
    username: '',
    isLoading: false,
    selected: [],
    selectedUser: null,
    roles: ['Admin', 'Member'],
    addModal: {
      title: 'Add User',
      button: 'Add User'
    },
    removeModal: {
      title: 'Remove User',
      button: 'Yes, remove'
    },
    headers: [
      {
        text: 'Name',
        align: 'left',
        sortable: false,
        value: 'name'
      },
      { text: 'Role', value: 'role' }
    ],
    users: [
      {
        name: 'Hiroki Nakayama',
        role: 'Admin'
      },
      {
        name: 'Takahiro Kubo',
        role: 'Member'
      },
      {
        name: 'Junya Kamura',
        role: 'Member'
      },
      {
        name: 'Yasufumi Taniguchi',
        role: 'Member'
      },
      {
        name: 'Ryo Sho',
        role: 'Member'
      }
    ],
    items: [
      {
        id: 1,
        username: 'Donald Trump',
        Description: 'Daily cat facts'
      },
      {
        id: 2,
        username: 'Barack Obama',
        Description: 'Pictures of cats from Tumblr'
      }
    ]
  }),

  watch: {
    username(val) {
      // Items have already been requested
      if (this.isLoading) return

      this.isLoading = true

      // Lazily load input items
      // GET /users endpoint
      // fetch('https://api.publicapis.org/entries')
      //   .then(res => res.json())
      //   .then((res) => {
      //     this.items.push({ username: 'Bush', id: this.items.length + 1 })
      //   })
      //   .catch((err) => {
      //     alert(err)
      //   })
      //   .finally(() => (this.isLoading = false))
    }
  },

  methods: {
    save() {
      // send server
    },
    openAddModal() {
      this.$refs.childDialogue.open()
    },
    openRemoveModal() {
      this.$refs.removeDialogue.open()
    }
  }

}
</script>
