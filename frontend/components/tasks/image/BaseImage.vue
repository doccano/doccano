<template>
  <v-image
    :config="{
      image: image
    }"
  />
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    imageUrl: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      image: new Image()
    }
  },

  watch: {
    imageUrl: {
      handler() {
        this.image.src = this.imageUrl
        this.image.onload = () => {
          this.$emit('loaded', this.image.width, this.image.height)
        }
      },
      immediate: true
    }
  }
})
</script>
