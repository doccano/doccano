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
                Add Label
              </v-btn>
              <Modal
                ref="childDialogue"
                :title="addModal.title"
                :button="addModal.button"
              >
                <v-text-field
                  label="Label name"
                  prepend-icon="label"
                />
                <v-select
                  :items="keys"
                  label="Key"
                  prepend-icon="mdi-keyboard"
                />
                <v-color-picker
                  v-model="color"
                  show-swatches
                  hide-mode-switch
                  width="800"
                  :mode.sync="mode"
                  class="ma-2"
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
                Are you sure you want to remove these labels from this project?
                <v-list dense>
                  <v-list-item v-for="(label, i) in selected" :key="i">
                    <v-list-item-content>
                      <v-list-item-title>{{ label.name }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </Modal>
            </v-card-title>
            <v-data-table
              v-model="selected"
              :headers="headers"
              :items="labels"
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
              <template v-slot:item.name="{ item }">
                <v-edit-dialog
                  :return-value.sync="item.name"
                >
                  {{ item.name }}
                  <template v-slot:input>
                    <v-text-field
                      v-model="item.name"
                      label="Edit"
                      single-line
                    />
                  </template>
                </v-edit-dialog>
              </template>
              <template v-slot:item.shortcut="{ item }">
                <v-edit-dialog
                  :return-value.sync="item.shortcut"
                  large
                  persistent
                  @save="save"
                >
                  <div>{{ item.shortcut }}</div>
                  <template v-slot:input>
                    <div class="mt-4 title">
                      Update key
                    </div>
                  </template>
                  <template v-slot:input>
                    <v-select
                      v-model="item.shortcut"
                      :items="keys"
                      label="Key"
                    />
                  </template>
                </v-edit-dialog>
              </template>
              <template v-slot:item.color="{ item }">
                <v-edit-dialog
                  :return-value.sync="item.color"
                  large
                  persistent
                  @save="save"
                >
                  <v-chip :color="item.color" dark>
                    {{ item.color }}
                  </v-chip>
                  <template v-slot:input>
                    <div class="mt-4 title">
                      Update color
                    </div>
                  </template>
                  <template v-slot:input>
                    <v-color-picker
                      v-model="item.color"
                      show-swatches
                      hide-mode-switch
                      width="800"
                      :mode.sync="mode"
                      class="ma-2"
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
    dialog: false,
    search: '',
    isLoading: false,
    selected: [],
    selectedUser: null,
    keys: 'abcdefghijklmnopqrstuvwxyz'.split(''),
    mode: 'hexa',
    color: '#FF00FF',
    addModal: {
      title: 'Add Label',
      button: 'Add Label'
    },
    removeModal: {
      title: 'Remove Label',
      button: 'Yes, remove'
    },
    headers: [
      {
        text: 'Name',
        align: 'left',
        value: 'name'
      },
      {
        text: 'Shortkey',
        value: 'shortcut'
      },
      {
        text: 'Color',
        sortable: false,
        value: 'color'
      }
    ],
    labels: [
      {
        id: 1,
        name: 'Location',
        color: '#E91E63',
        shortcut: 'l',
        fat: 6.0
      },
      {
        id: 2,
        name: 'Organization',
        color: '#03A9F4',
        shortcut: 'o',
        fat: 9.0
      },
      {
        id: 3,
        name: 'Person',
        color: '#009688',
        shortcut: 'p',
        fat: 16.0
      },
      {
        id: 4,
        name: 'Money',
        color: '#FF6F00',
        shortcut: 'm',
        fat: 3.7
      },
      {
        id: 5,
        name: 'Other',
        color: '#333333',
        shortcut: 't',
        fat: 16.0
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
