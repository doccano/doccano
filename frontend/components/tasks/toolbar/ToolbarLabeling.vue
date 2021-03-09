<template>
  <v-toolbar
    class="pa-0"
    dense
    flat
  >
    <v-row no-gutters>
      <v-btn-toggle>
        <button-review
          :is-reviewd="isReviewd"
          @click:review="$emit('click:review')"
        />

        <button-filter
          :value="filterOption"
          @click:filter="$emit('click:filter', $event)"
        />

        <button-guideline
          @click:guideline="$emit('click:guideline')"
        />

        <button-comment
          @click:comment="$emit('click:comment')"
        />

        <button-auto-labeling
          @click:auto="$emit('click:auto')"
        />

        <button-clear
          @click:clear="$emit('click:clear')"
        />
      </v-btn-toggle>
    </v-row>
    <v-row>

    </v-row>
  </v-toolbar>
</template>

<script lang="ts">
import Vue from 'vue'
import ButtonAutoLabeling from './buttons/ButtonAutoLabeling.vue'
import ButtonClear from './buttons/ButtonClear.vue'
import ButtonComment from './buttons/ButtonComment.vue'
import ButtonFilter from './buttons/ButtonFilter.vue'
import ButtonGuideline from './buttons/ButtonGuideline.vue'
import ButtonReview from './buttons/ButtonReview.vue'

export default Vue.extend({
  components: {
    ButtonAutoLabeling,
    ButtonClear,
    ButtonComment,
    ButtonFilter,
    ButtonGuideline,
    ButtonReview,
  },

  props: {
    filterOption: {
      type: String,
      default: ''
    },
    isReviewd: {
      type: Boolean,
      default: false
    }
  }
})
</script>

<style scoped>
::v-deep .v-toolbar__content {
  padding: 0;
}
</style>