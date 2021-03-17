<template>
  <v-bottom-navigation
    app
    absolute
    hide-on-scroll
  >
    <v-btn
      :disabled="isFirstPage"
      @click="updatePage(page - 1)"
    >
      <span>Prev</span>
      <v-icon>mdi-chevron-left</v-icon>
    </v-btn>

    <v-btn
      :disabled="isLastPage"
      @click="updatePage(page + 1)"
    >
      <span>Next</span>
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    total: {
      type: Number,
      default: 1,
      required: true
    }
  },

  computed: {
    page(): number {
      // @ts-ignore
      return parseInt(this.$route.query.page, 10)
    },
    isFirstPage(): boolean {
      return this.page === 1
    },
    isLastPage(): boolean {
      return this.page === this.total || this.total === 0
    }
  },

  methods: {
    updatePage(page: number) {
      this.$router.push({ query: { page: page.toString() }})
    }
  }
})
</script>
