<template>
  <v-data-table
    :headers="headers"
    :items="metaArray"
    item-key="key"
    hide-default-footer
    :no-data-text="$t('vuetify.noDataAvailable')"
    disable-pagination
    class="elevation-1"
  />
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
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
          text: this.$t('annotation.key'),
          align: 'left',
          value: 'key',
          sortable: false
        },
        {
          text: this.$t('annotation.value'),
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
})
</script>
