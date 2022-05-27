<template>
  <v-data-table :headers="headers" :items="value">
    <template #top>
      <v-dialog v-model="dialog" max-width="800px">
        <template #activator="{ on, attrs }">
          <v-btn color="primary" dark class="text-none" v-bind="attrs" v-on="on"> Add </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">Add a new mapping</span>
          </v-card-title>

          <v-card-text>
            <v-container>
              <v-form ref="form" v-model="valid">
                <v-row>
                  <v-col cols="12" sm="12" class="pa-0">
                    <v-text-field
                      v-model="editedItem.from"
                      label="From"
                      :rules="labelNameRules($t('rules.labelNameRules'))"
                      outlined
                    />
                  </v-col>
                  <v-col cols="12" sm="12" class="pa-0">
                    <v-select
                      v-model="editedItem.to"
                      :items="items"
                      :rules="labelNameRules($t('rules.labelNameRules'))"
                      label="To"
                      outlined
                    />
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
import { labelNameRules } from '@/rules/index'

export default Vue.extend({
  props: {
    value: {
      type: Array,
      default: () => [],
      required: true
    }
  },
  data() {
    return {
      dialog: false,
      headers: [
        {
          text: 'From',
          align: 'left',
          value: 'from',
          sortable: false
        },
        {
          text: 'To',
          align: 'left',
          value: 'to',
          sortable: false
        },
        {
          text: 'Actions',
          value: 'actions',
          sortable: false
        }
      ],
      valid: false,
      editedIndex: -1,
      editedItem: {
        from: '',
        to: ''
      },
      defaultItem: {
        from: '',
        to: ''
      },
      items: [] as string[],
      labelNameRules,
      mdiPencil,
      mdiDelete
    }
  },

  async created() {
    const project = await this.$services.project.findById(this.$route.params.id)
    if (project.projectType.endsWith('Classification')) {
      const labels = await this.$services.categoryType.list(this.$route.params.id)
      this.items = labels.map((item) => item.text)
    } else {
      const labels = await this.$services.spanType.list(this.$route.params.id)
      this.items = labels.map((item) => item.text)
    }
  },

  methods: {
    editItem(item: { from: string; to: string }) {
      this.editedIndex = this.value.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem(item: { from: string; to: string }) {
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
      this.$emit('input', items)
      this.close()
    }
  }
})
</script>
