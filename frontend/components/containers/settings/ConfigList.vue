<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="items"
    :loading="loading"
    :no-data-text="$t('vuetify.noDataAvailable')"
    item-key="id"
    :loading-text="$t('generic.loading')"
    show-select
    @input="updateSelected"
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
            class="mb-2"
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
    <template v-slot:item.model_attrs="{ item }">
      <pre>{{ JSON.stringify(item.model_attrs, null, 4) }}</pre>
    </template>
    <template v-slot:item.label_mapping="{ item }">
      <pre>{{ JSON.stringify(item.label_mapping, null, 4) }}</pre>
    </template>
  </v-data-table>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'
import ConfigService from '@/services/config.service'

export default {
  fetch() {
    this.loading = true
    ConfigService.getConfigList({
      projectId: this.$route.params.id
    }).then((response) => {
      this.items = response.data
    }).catch((error) => {
      alert(error)
    })
    this.loading = false
  },

  data() {
    return {
      loading: false,
      options: {},
      items: [],
      selected: [],
      dialog: false,
      headers: [
        {
          text: 'Model name',
          align: 'left',
          value: 'model_name',
          sortable: false
        },
        {
          text: 'Attributes',
          align: 'left',
          value: 'model_attrs',
          sortable: false
        },
        {
          text: 'Mapping',
          align: 'left',
          value: 'label_mapping',
          sortable: false
        }
      ]
    }
  },

  methods: {
    ...mapActions('documents', ['getDocumentList', 'updateDocument']),
    ...mapMutations('documents', ['updateSelected']),

    handleUpdateDocument(payload) {
      const data = {
        projectId: this.$route.params.id,
        ...payload
      }
      this.updateDocument(data)
    }
  }
}
</script>
