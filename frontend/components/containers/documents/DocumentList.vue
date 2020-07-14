<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="items"
    :options.sync="options"
    :server-items-length="total"
    :search="search"
    :loading="loading"
    :footer-props="{
      'items-per-page-options': [10, 50, 100]
    }"
    item-key="id"
    loading-text="Loading... Please wait"
    show-select
    @input="updateSelected"
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
            @change="handleUpdateDocument({ id: item.id, text: $event })"
          />
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.action="{ item }">
      <v-btn
        small
        color="primary text-capitalize"
        @click="toLabeling(item)"
      >
        Annotate
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'

export default {
  async fetch() {
    await this.getDocumentList({
      projectId: this.$route.params.id,
      ...this.$route.query
    })
  },

  data() {
    return {
      search: '',
      options: {},
      headers: [
        {
          text: 'Text',
          align: 'left',
          value: 'text',
          sortable: false
        },
        {
          text: 'Metadata',
          align: 'left',
          value: 'meta',
          sortable: false
        },
        {
          text: 'Action',
          align: 'left',
          value: 'action',
          sortable: false
        }
      ]
    }
  },

  computed: {
    ...mapState('documents', ['items', 'selected', 'loading', 'total']),
    ...mapGetters('projects', ['getLink'])
  },

  watch: {
    '$route.query': '$fetch',
    options: {
      handler(newvalue, oldvalue) {
        this.$router.push({
          query: {
            limit: this.options.itemsPerPage,
            offset: (this.options.page - 1) * this.options.itemsPerPage,
            q: this.search
          }
        })
      },
      deep: true
    },
    search() {
      this.$router.push({
        query: {
          limit: this.options.itemsPerPage,
          offset: 0,
          q: this.search
        }
      })
      this.options.page = 1
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
    },

    toLabeling(doc) {
      const index = this.items.findIndex(item => item.id === doc.id)
      const offset = (this.options.page - 1) * this.options.itemsPerPage
      const page = offset + index + 1
      this.$router.push({
        path: `/projects/${this.$route.params.id}/${this.getLink}`,
        query: {
          page,
          q: this.search
        }
      })
    }
  }
}
</script>
