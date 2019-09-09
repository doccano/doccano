<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="docs"
    item-key="id"
    :search="search"
    :loading="loading"
    loading-text="Loading... Please wait"
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
        <span class="d-flex d-sm-none">{{ item.text | truncate(50) }}</span>
        <span class="d-none d-sm-flex">{{ item.text | truncate(200) }}</span>
        <template v-slot:input>
          <v-textarea
            :value="item.text"
            label="Edit"
            autofocus
            @change="updateDocument({ id: item.id, text: $event })"
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
    docs: {
      type: Array,
      default: () => [],
      required: true
    },
    selected: {
      type: Array,
      default: () => [],
      required: true
    },
    loading: {
      type: Boolean,
      default: false,
      required: true
    }
  },
  data() {
    return {
      search: ''
    }
  },
  methods: {
    update(selected) {
      this.$emit('update-selected', selected)
    },
    updateDocument(payload) {
      this.$emit('update-doc', payload)
    }
  }
}
</script>
