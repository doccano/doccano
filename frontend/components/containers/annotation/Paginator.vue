<template>
  <div class="v-data-footer">
    <span>
      {{ page }} of {{ total }}
    </span>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-shortkey.once="['arrowleft']"
          text
          :disabled="page===1"
          fab
          small
          v-on="on"
          @shortkey="prevPage"
          @click="prevPage"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </template>
      <span>←</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-shortkey.once="['arrowright']"
          text
          :disabled="page===total"
          fab
          small
          v-on="on"
          @shortkey="nextPage(total)"
          @click="nextPage(total)"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </template>
      <span>→</span>
    </v-tooltip>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'
Vue.use(require('vue-shortkey'))

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
