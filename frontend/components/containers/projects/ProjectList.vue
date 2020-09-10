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
      'items-per-page-text': $t('vuetify.itemsPerPageText')
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
      <nuxt-link :to="`/projects/${item.id}`">
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
          text: 'Name',
          align: 'left',
          value: 'name'
        },
        {
          text: 'Description',
          value: 'description'
        },
        {
          text: 'Type',
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
