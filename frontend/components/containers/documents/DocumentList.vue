<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="items"
    item-key="id"
    :options.sync="options"
    :server-items-length="total"
    :search="search"
    :loading="loading"
    :footer-props="{
      'items-per-page-options': [10, 50, 100]
    }"
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
        @click="$router.push('/projects')"
      >
        Annotate
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'

export default {
  data() {
    return {
      search: '',
      options: {}
    }
  },

  computed: {
    ...mapState('documents', ['items', 'selected', 'loading', 'total']),
    ...mapGetters('documents', ['headers'])
  },

  watch: {
    options: {
      handler() {
        this.getDocumentList({
          projectId: this.$route.params.id,
          limit: this.options.itemsPerPage,
          offset: (this.options.page - 1) * this.options.itemsPerPage
        })
      },
      deep: true
    },
    search() {
      this.getDocumentList({
        projectId: this.$route.params.id,
        q: this.search
      })
    }
  },

  created() {
    this.getDocumentList({
      projectId: this.$route.params.id
    })
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
