<template>
  <v-form>
    <v-textarea
      v-model="message"
      auto-grow
      hide-details
      outlined
      autofocus
      rows="1"
      name="CommentInput"
      :label="$t('comments.message')"
    />
    <v-btn
      class="white--text text-capitalize mt-3"
      color="primary"
      depressed
      :disabled="isCommentEmpty"
      @click="addComment"
    >
      {{ $t("comments.send") }}
    </v-btn>
  </v-form>
</template>

<script lang="ts">
import Vue from "vue";
import _ from 'lodash'

export default Vue.extend({
  data() {
    return {
      message: "",
    };
  },

  computed: {
    isCommentEmpty() {
      return _.get(this,"message","").trim() === "";
    },
  },

  methods: {
    addComment() {
      this.$emit("add-comment", this.message);
      this.message = "";
    },
  },
});
</script>
