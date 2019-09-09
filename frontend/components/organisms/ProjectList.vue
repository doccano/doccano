<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="projects"
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
    <template v-slot:item.name="{ item }">
      <nuxt-link :to="`/projects/${item.id}`">
        <span>{{ item.name }}</span>
      </nuxt-link>
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
    projects: {
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
      this.$emit('update', selected)
    }
  }
}
</script>
