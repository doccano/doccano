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
                Are you sure you want to remove these documents from this project?
                <v-list dense>
                  <v-list-item v-for="(doc, i) in selected" :key="i">
                    <v-list-item-content>
                      <v-list-item-title>{{ doc.text | truncate(50) }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </Modal>
            </v-card-title>
            <v-data-table
              v-model="selected"
              :headers="headers"
              :items="docs"
              item-key="id"
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
              <template v-slot:item.text="{ item }">
                <v-edit-dialog
                  :return-value.sync="item.text"
                  large
                >
                  <span class="d-flex d-sm-none">{{ item.text | truncate(50) }}</span>
                  <span class="d-none d-sm-flex">{{ item.text | truncate(200) }}</span>
                  <!--{{ item.text | truncate(200) }}-->
                  <template v-slot:input>
                    <v-textarea
                      v-model="item.text"
                      label="Edit"
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
    selected: [],
    removeModal: {
      title: 'Remove Document',
      button: 'Yes, remove'
    },
    headers: [
      {
        text: 'Text',
        align: 'left',
        value: 'text'
      }
    ],
    docs: [
      {
        id: 1,
        text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
      },
      {
        id: 2,
        text: 'Text 1'
      },
      {
        id: 3,
        text: 'Text 2'
      },
      {
        id: 4,
        text: 'Text 3'
      },
      {
        id: 5,
        text: 'Text 4'
      }
    ]
  }),

  methods: {
    save() {
      // send server
    },
    cancel() {
    },
    open() {
    },
    close() {
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
