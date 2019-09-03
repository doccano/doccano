<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="labels"
    item-key="id"
    :search="search"
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
      <v-edit-dialog
        :return-value.sync="item.text"
      >
        {{ item.text }}
        <template v-slot:input>
          <v-text-field
            v-model="item.text"
            label="Edit"
            single-line
          />
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.suffix_key="{ item }">
      <v-edit-dialog
        :return-value.sync="item.suffix_key"
        large
        persistent
        @save="updateShortcut({ id: item.id, suffix_key: newKey })"
      >
        <div>{{ item.suffix_key }}</div>
        <template v-slot:input>
          <div class="mt-4 title">
            Update key
          </div>
        </template>
        <template v-slot:input>
          <v-select
            :value="item.suffix_key"
            :items="keys"
            label="Key"
            @input="setNewKey"
          />
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.background_color="{ item }">
      <v-edit-dialog
        :return-value.sync="item.background_color"
        large
        persistent
        @save="updateColor({ id:item.id, background_color: newColor })"
      >
        <v-chip :color="item.background_color" dark>
          {{ item.background_color }}
        </v-chip>
        <template v-slot:input>
          <div class="mt-4 title">
            Update color
          </div>
        </template>
        <template v-slot:input>
          <v-color-picker
            :value="item.backgroundColor"
            show-swatches
            hide-mode-switch
            width="800"
            :mode.sync="mode"
            class="ma-2"
            @input="setNewColor"
          />
        </template>
      </v-edit-dialog>
    </template>
  </v-data-table>
</template>

<script>
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
    }
  },
  data() {
    return {
      search: '',
      newKey: null,
      newColor: null,
      keys: 'abcdefghijklmnopqrstuvwxyz'.split(''),
      mode: 'hexa',
      color: '#FF00FF'
    }
  },
  methods: {
    setNewKey(value) {
      this.newKey = value
    },
    setNewColor(value) {
      this.newColor = value
    },
    update(selected) {
      this.$emit('update-selected', selected)
    },
    updateRole(payload) {
      this.$emit('update-role', payload)
    },
    updateShortcut(payload) {
      this.$emit('update-label', payload)
    },
    updateColor(payload) {
      this.$emit('update-label', payload)
    }
  }
}
</script>
