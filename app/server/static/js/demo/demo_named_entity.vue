<template lang="pug">
extends ../annotation.pug

block annotation-area
  div.card
    header.card-header
      div.card-header-title.has-background-royalblue
        div.field.is-grouped.is-grouped-multiline
          div.control(v-for="label in labels")
            div.tags.has-addons
              a.tag.is-medium(
                v-shortkey.once="[ label.shortcut ]"
                v-bind:style="{ \
                  color: label.text_color, \
                  backgroundColor: label.background_color \
                }"
                v-on:click="annotate(label.id)"
                v-on:shortkey="annotate(label.id)"
              ) {{ label.text }}
              span.tag.is-medium {{ label.shortcut }}

    div.card-content
      div.content(v-if="docs[pageNumber] && annotations[pageNumber]")
        annotator(
          v-bind:labels="labels"
          v-bind:entity-positions="annotations[pageNumber]"
          v-bind:text="docs[pageNumber].text"
          v-on:remove-label="removeLabel"
          v-on:add-label="addLabel"
          ref="annotator"
        )
</template>

<style scoped>
.card-header-title {
  padding: 1.5rem;
}
</style>

<script>
import { demoNamedEntity } from './demo_data';
import annotationMixin from './demo_mixin';
import Annotator from './demo_annotator.vue';

export default {
  components: { Annotator },

  mixins: [annotationMixin],

  data: () => ({ ...demoNamedEntity }),

  methods: {
    annotate(labelId) {
      this.$refs.annotator.addLabel(labelId);
    },

    addLabel(annotation) {
      this.annotations[this.pageNumber].push(annotation);
    },
  },
};
</script>
