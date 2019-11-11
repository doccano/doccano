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
          @shortkey="nextPage"
          @click="nextPage"
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
import { mapState, mapActions, mapMutations } from 'vuex'
Vue.use(require('vue-shortkey'))

export default {
  data() {
    return {
      page: 1,
      limit: 10
    }
  },

  computed: {
    ...mapState('documents', ['items', 'total']),

    offset() {
      return Math.floor((this.page - 1) / this.limit) * this.limit
    },

    current() {
      return (this.page - 1) % this.limit
    }
  },

  watch: {
    page() {
      const checkpoint = {}
      checkpoint[this.$route.params.id] = this.page
      localStorage.setItem('checkpoint', JSON.stringify(checkpoint))
    },
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
    const checkpoint = JSON.parse(localStorage.getItem('checkpoint'))
    this.page = checkpoint[this.$route.params.id] ? checkpoint[this.$route.params.id] : 1
    this.getDocumentList({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('documents', ['getDocumentList']),
    ...mapMutations('documents', ['setCurrent', 'updateSearchOptions']),
    prevPage() {
      this.page = Math.max(this.page - 1, 1)
    },
    nextPage() {
      this.page = Math.min(this.page + 1, this.total)
    }
  }
}
</script>
