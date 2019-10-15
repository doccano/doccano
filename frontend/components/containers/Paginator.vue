<template>
  <v-pagination
    v-model="page"
    :length="total"
    :total-visible="7"
  />
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex'

export default {
  data() {
    return {
      page: 1,
      limit: 5
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
      this.getDocumentList({
        projectId: this.$route.params.id,
        limit: this.limit,
        offset: this.offset
      })
    },
    current() {
      this.setCurrent(this.current)
    }
  },

  created() {
    const checkpoint = JSON.parse(localStorage.getItem('checkpoint'))
    this.page = checkpoint ? checkpoint[this.$route.params.id] : 1
    this.getDocumentList({
      projectId: this.$route.params.id,
      limit: this.limit,
      offset: this.offset
    })
  },

  methods: {
    ...mapActions('documents', ['getDocumentList']),
    ...mapMutations('documents', ['setCurrent'])
  }
}
</script>
