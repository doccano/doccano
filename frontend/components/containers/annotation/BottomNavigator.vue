<template>
  <v-bottom-navigation
    app
    absolute
    hide-on-scroll
  >
    <v-btn
      :disabled="value===1"
      @click="prevPage"
    >
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

    <v-btn
      :disabled="value===length || length===0"
      @click="nextPage"
    >
      <span>Next</span>
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
export default {
  props: {
    value: {
      type: Number,
      default: 1,
      required: true
    },
    length: {
      type: Number,
      default: 1,
      required: true
    }
  },

  methods: {
    prevPage() {
      const page = Math.max(this.value - 1, 1)
      this.$emit('input', page)
    },
    nextPage() {
      const page = Math.min(this.value + 1, this.length)
      this.$emit('input', page)
    }
  }
}
</script>
