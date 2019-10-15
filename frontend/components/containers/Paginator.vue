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
