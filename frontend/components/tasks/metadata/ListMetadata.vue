<template>
  <v-data-table
    :headers="headers"
    :items="metaArray"
    item-key="key"
    hide-default-footer
    :no-data-text="$t('vuetify.noDataAvailable')"
    disable-pagination
    class="elevation-1"
  >
    <template #[`item.value`]="{ item }">
      <template v-if="item.key.indexOf('im_url') > -1">
        <a :href="item.value" target="_blank"><img :src="item.value" style="height: 250px" /></a>
      </template>
      <template v-else-if="item.key.indexOf('url') > -1">
        <a :href="item.value" target="_blank">{{ item.value }}</a>
      </template>
      <template v-else>
        {{ item.value }}
      </template>
    </template>
  </v-data-table>
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
