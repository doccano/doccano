<template>
  <v-bottom-navigation
    absolute
    hide-on-scroll
    background-color="transparent"
    class="elevation-0"
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

    <v-btn @click="nextPage">
      <span>Next</span>
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'

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
