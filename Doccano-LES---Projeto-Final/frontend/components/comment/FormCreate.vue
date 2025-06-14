<template>
  <v-form v-model="valid">
    <v-textarea
      v-model="message"
      auto-grow
      hide-details
      outlined
      rows="1"
      name="CommentInput"
      :label="$t('comments.message')"
      :rules="commentRules"
    />
    <v-btn
      class="white--text text-capitalize mt-3"
      color="primary"
      depressed
      :disabled="!valid"
      @click="addComment"
    >
      {{ $t('comments.send') }}
    </v-btn>
  </v-form>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      commentRules: [(v: string) => !!v.trim() || 'Comment is required'],
      message: '',
      valid: false
    }
  },

  methods: {
    addComment() {
      this.$emit('add-comment', this.message)
      this.message = ''
    }
  }
})
</script>
