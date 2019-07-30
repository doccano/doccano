<template lang="pug">
extends ./annotation.pug

block annotation-area
  div.card
    header.card-header
      div.card-header-title.has-background-royalblue
        div.field.is-grouped.is-grouped-multiline
          div.control
            div.tags.has-addons.white(
              v-if="docs[pageNumber] && docs[pageNumber].extra_text"
              ) {{ docs[pageNumber].extra_text || 'missing quesiton' }}

    div.card-content
      div.content(v-if="docs[pageNumber] && annotations[pageNumber]")
        annotator(
          v-bind:labels="labels"
          v-bind:entity-positions="annotations[pageNumber]"
          v-bind:text="docs[pageNumber].text"
          v-on:remove-answer="removeLabel"
          v-on:add-answer="addAnswer"
          ref="annotator"
        )
    div.card-content.has-text-centered
      button.button.is-link.is-medium(
        v-bind:disabled="this.hasAnswer"
        v-on:click="annotate()") Submit Selection
</template>

<style scoped>
.card-header-title {
  padding: 1.5rem;
}
.white {
  color: white
}
</style>

<script>
import annotationMixin from './annotationMixin';
import Annotator from './annotator_qanda.vue';
import HTTP from './http';
import { simpleShortcut } from './filter';

export default {
  filters: { simpleShortcut },

  components: { Annotator },

  mixins: [annotationMixin],

  computed: {
    hasAnswer() {
      return this.docs[this.pageNumber] && this.annotations[this.pageNumber].length > 0;
    },
  },

  methods: {
    annotate() {
      this.$refs.annotator.addAnswer();
    },

    addAnswer(answer) {
      const docId = this.docs[this.pageNumber].id;
      HTTP.post(`docs/${docId}/annotations`, answer).then((response) => {
        this.annotations[this.pageNumber].push(response.data);
      });
    },

    async submit() {
      const state = this.getState();
      this.url = `docs?q=${this.searchQuery}&seq_annotations__isnull=${state}&offset=${this.offset}`;
      await this.search();
      this.pageNumber = 0;
    },
  },
};
</script>
