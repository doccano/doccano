<template>
  <v-data-table
    :value="selectedComments"
    :headers="headers"
    :items="comments"
    :search="search"
    :options.sync="options"
    :server-items-length="totalComments"
    :loading="loading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      'showFirstLastPage': true,
      'items-per-page-options': [5, 10, 15, 100],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="updateSelectedComments"
  >
    <template v-slot:item.created_at="{ item }">
      <span>{{ item.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD HH:mm') }}</span>
    </template>
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
  </v-data-table>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapGetters, mapState, mapMutations } from 'vuex'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
Vue.use(VueFilterDateFormat)
Vue.use(VueFilterDateParse)

export default {
  async fetch() {
    await this.getProjectCommentList({
      projectId: this.$route.params.id
    })
  },
  data() {
    return {
      search: this.$route.query.q,
      options: {},
      headers: [
        {
          text: this.$t('comments.created_at'),
          align: 'left',
          value: 'created_at'
        },
        {
          text: this.$t('comments.document'),
          value: 'document_text'
        },
        {
          text: this.$t('user.username'),
          value: 'username'
        },
        {
          text: this.$t('dataset.text'),
          value: 'text'
        }
      ]
    }
  },
  computed: {
    ...mapState('comments', ['comments', 'loading', 'selectedComments', 'totalComments']),
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
    ...mapActions('comments', ['getProjectCommentList']),
    ...mapMutations('comments', ['updateSelectedComments'])
  }

}
</script>
