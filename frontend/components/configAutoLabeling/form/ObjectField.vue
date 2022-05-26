<template>
  <v-data-table :headers="headers" :items="value">
    <template #top>
      <v-toolbar class="toolbar-control" flat>
        <v-toolbar-title class="text-capitalize">
          {{ title }}
        </v-toolbar-title>
        <v-spacer />
        <v-dialog v-model="dialog" max-width="800px">
          <template #activator="{ on, attrs }">
            <v-btn color="primary" dark class="text-none" v-bind="attrs" v-on="on"> Add </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">Add a new field</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-form ref="form" v-model="valid">
                  <v-row>
                    <v-col cols="12" sm="12" class="pa-0">
                      <v-text-field v-model="editedItem.key" label="Key" outlined />
                    </v-col>
                    <v-col cols="12" sm="12" class="pa-0">
                      <v-text-field v-model="editedItem.value" label="Value" outlined />
                    </v-col>
                  </v-row>
                </v-form>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn color="blue darken-1" class="text-capitalize" text @click="close">
                Cancel
              </v-btn>
              <v-btn
                :disabled="!valid"
                color="blue darken-1"
                class="text-capitalize"
                text
                @click="save"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template #[`item.actions`]="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">
        {{ mdiPencil }}
      </v-icon>
      <v-icon small @click="deleteItem(item)">
        {{ mdiDelete }}
      </v-icon>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiPencil, mdiDelete } from '@mdi/js'

export default Vue.extend({
  props: {
    value: {
      type: Array,
      default: () => [],
      required: true
    },
    title: {
      type: String,
      default: '',
      required: true
    }
  },
  data() {
    return {
      headers: [
        {
          text: 'Key',
          align: 'left',
          value: 'key',
          sortable: false
        },
        {
          text: 'Value',
          align: 'left',
          value: 'value',
          sortable: false
        },
        {
          text: 'Actions',
          value: 'actions',
          sortable: false
        }
      ],
      dialog: false,
      valid: false,
      editedIndex: -1,
      editedItem: {
        key: '',
        value: ''
      },
      defaultItem: {
        key: '',
        value: ''
      },
      items: [] as string[],
      mdiPencil,
      mdiDelete
    }
  },

  methods: {
    editItem(item: { key: string; value: string }) {
      this.editedIndex = this.value.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem(item: { key: string; value: string }) {
      this.editedIndex = this.value.indexOf(item)
      this.editedItem = Object.assign({}, item)
      const items = Object.assign([], this.value)
      items.splice(this.editedIndex, 1)
      this.editedItem = Object.assign({}, this.defaultItem)
      this.editedIndex = -1
      this.$emit('input', items)
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save() {
      const items = Object.assign([], this.value)
      if (this.editedIndex > -1) {
        Object.assign(items[this.editedIndex], this.editedItem)
      } else {
        items.push(this.editedItem)
      }
      this.close()
      this.$emit('input', items)
    }
  }
})
</script>

<style scoped>
.toolbar-control >>> .v-toolbar__content {
  padding: 0px !important;
}
</style>
