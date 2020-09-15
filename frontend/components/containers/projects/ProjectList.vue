<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="projects"
    :search="search"
    :loading="loading"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      'showFirstLastPage': true,
      'items-per-page-options': [5, 10, 15, $t('generic.all')],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="update"
  >
    <template v-slot:top>
      <v-text-field
        v-model="search"
        prepend-inner-icon="search"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <template v-slot:item.name="{ item }">
      <nuxt-link :to="localePath(`/projects/${item.id}`)">
        <span>{{ item.name }}</span>
      </nuxt-link>
    </template>
  </v-data-table>
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'

export default {
  data() {
    return {
      search: '',
      headers: [
        {
          text: this.$t('generic.name'),
          align: 'left',
          value: 'name'
        },
        {
          text: this.$t('generic.description'),
          value: 'description'
        },
        {
          text: this.$t('generic.type'),
          value: 'project_type'
        }
      ]
    }
  },

  computed: {
    ...mapState('projects', ['projects', 'selected', 'loading'])
  },

  async created() {
    await this.getProjectList()
  },

  methods: {
    ...mapActions('projects', ['getProjectList']),
    ...mapMutations('projects', ['updateSelected']),

    update(selected) {
      this.updateSelected(selected)
    }
  }
}
</script>
