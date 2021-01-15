<template>
  <v-bottom-navigation
    app
    absolute
    hide-on-scroll
  >
    <v-btn @click="prevPage">
      <span>Prev</span>
      <v-icon>mdi-chevron-left</v-icon>
    </v-btn>

    <!-- <v-btn @click="approveDocument">
      <span>Done</span>
      <v-icon v-if="approved">
        mdi-check
      </v-icon>
      <v-icon v-else>
        mdi-close
      </v-icon>
    </v-btn>

    <v-btn value="guide">
      <span>Guideline</span>
      <v-icon>mdi-book-open-outline</v-icon>
    </v-btn> -->

    <v-btn @click="nextPage(total)">
      <span>Next</span>
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'

export default {
  computed: {
    ...mapState('documents', ['items', 'total']),
    ...mapGetters('pagination', ['current', 'limit', 'offset', 'page'])
  },

  watch: {
    offset() {
      this.updateSearchOptions({
        limit: this.limit,
        offset: this.offset
      })
      this.getDocumentList({
        projectId: this.$route.params.id
      })
    },
    current() {
      this.setCurrent(this.current)
    }
  },

  created() {
    this.initPage({
      projectId: this.$route.params.id
    })
    this.getDocumentList({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('documents', ['getDocumentList']),
    ...mapActions('pagination', ['prevPage', 'nextPage', 'initPage']),
    ...mapMutations('documents', ['setCurrent', 'updateSearchOptions'])
  }
}
</script>
