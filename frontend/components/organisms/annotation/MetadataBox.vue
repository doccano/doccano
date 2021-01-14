<template>
  <v-data-table
    :headers="headers"
    :items="metaArray"
    item-key="key"
    hide-default-footer
    disable-pagination
    class="elevation-1"
  />
</template>

<script>
export default {
  props: {
    metadata: {
      type: Object,
      default: () => ({}),
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
        }
      ]
    }
  },

  computed: {
    metaArray() {
      const items = []
      for (const [key, value] of Object.entries(this.metadata)) {
        items.push({
          key,
          value
        })
      }
      return items
    }
  }
}
</script>
