<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="labels"
    :search="search"
    :loading="loading"
    loading-text="Loading... Please wait"
    item-key="id"
    show-select
    @input="update"
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
      <v-edit-dialog>
        {{ item.text }}
        <template v-slot:input>
          <v-text-field
            :value="item.text"
            :rules="labelNameRules"
            label="Edit"
            single-line
            @change="updateLabel({ id: item.id, text: $event })"
          />
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.suffix_key="{ item }">
      <v-edit-dialog>
        <div>{{ item.suffix_key }}</div>
        <template v-slot:input>
          <v-select
            :value="item.suffix_key"
            :items="keys"
            label="Key"
            @change="updateLabel({ id: item.id, suffix_key: $event })"
          />
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.background_color="{ item }">
      <v-edit-dialog>
        <v-chip :color="item.background_color" dark>
          {{ item.background_color }}
        </v-chip>
        <template v-slot:input>
          <v-color-picker
            :value="item.backgroundColor"
            :rules="colorRules"
            show-swatches
            hide-mode-switch
            width="800"
            mode="hexa"
            class="ma-2"
            @update:color="updateLabel({ id:item.id, background_color: $event.hex })"
          />
        </template>
      </v-edit-dialog>
    </template>
  </v-data-table>
</template>

<script>
import { colorRules, labelNameRules } from '@/rules/index'

export default {
  props: {
    headers: {
      type: Array,
      default: () => [],
      required: true
    },
    labels: {
      type: Array,
      default: () => [],
      required: true
    },
    selected: {
      type: Array,
      default: () => [],
      required: true
    },
    keys: {
      type: Array,
      default: () => 'abcdefghijklmnopqrstuvwxyz'.split('')
    },
    loading: {
      type: Boolean,
      default: false,
      required: true
    }
  },
  data() {
    return {
      search: '',
      colorRules,
      labelNameRules
    }
  },
  methods: {
    update(selected) {
      this.$emit('update-selected', selected)
    },
    updateLabel(payload) {
      this.$emit('update-label', payload)
    }
  }
}
</script>
