<template>
  <v-data-table
    v-model="selected"
    :headers="headers"
    :items="items.toArray()"
    :loading="loading"
    :no-data-text="$t('vuetify.noDataAvailable')"
    item-key="id"
    :loading-text="$t('generic.loading')"
    show-select
  >
    <template v-slot:top>
      <v-dialog
        v-model="dialog"
        max-width="500px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            dark
            class="ma-4 text-capitalize"
            v-bind="attrs"
            v-on="on"
          >
            Create
          </v-btn>
        </template>
        <v-card>
          hoge
        </v-card>
      </v-dialog>
    </template>
    <template v-slot:item.modelAttrs="{ item }">
      <pre>{{ JSON.stringify(item.modelAttrs, null, 4) }}</pre>
    </template>
    <template v-slot:item.labelMapping="{ item }">
      <pre>{{ JSON.stringify(item.labelMapping, null, 4) }}</pre>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from 'vue'
import { headers, ConfigItemList } from '@/models/config/config-item-list'
import { FromApiConfigItemListRepository } from '@/repositories/config/api'

export default Vue.extend({

  data() {
    return {
      loading: false,
      options: {},
      items: ConfigItemList.valueOf([]),
      selected: [],
      dialog: false,
      headers
    }
  },

  async created() {
    this.loading = true
    const configRepository = new FromApiConfigItemListRepository()
    this.items = await configRepository.list(this.$route.params.id)
    this.loading = false
  },

  methods: {
  }
})
</script>
