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
                v-on:click="addLabel(label)"
                v-on:shortkey="addLabel(label)"
              ) {{ label.text }}
              span.tag.is-medium {{ label.shortcut }}

    div.card-content
      div.field.is-grouped.is-grouped-multiline
        div.control(v-for="annotation in annotations[pageNumber]")
          div.tags.has-addons
            span.tag.is-medium(
              v-bind:style="{ \
                color: id2label[annotation.label].text_color, \
                backgroundColor: id2label[annotation.label].background_color \
              }"
            ) {{ id2label[annotation.label].text }}
              button.delete.is-small(v-on:click="removeLabel(annotation)")

      hr
      div.content(v-if="docs[pageNumber]") {{ docs[pageNumber].text }}
</template>

<style scoped>
.card-header-title {
  padding: 1.5rem;
}

hr {
  margin: 0.8rem 0;
}
</style>

<script>
import annotationMixin from './demo_mixin';
import { demoTextClassification } from './demo_data';

export default {
  mixins: [annotationMixin],

  data: () => ({ ...demoTextClassification }),

  methods: {
    isIn(label) {
      for (let i = 0; i < this.annotations[this.pageNumber].length; i++) {
        const a = this.annotations[this.pageNumber][i];
        if (a.label === label.id) {
          return a;
        }
      }
      return false;
    },

    addLabel(label) {
      const a = this.isIn(label);
      if (a) {
        this.removeLabel(a);
      } else {
        const annotation = {
          id: this.annotationId++,
          label: label.id,
        };
        this.annotations[this.pageNumber].push(annotation);
        console.log(this.annotations); // eslint-disable-line no-console
      }
    },
  },
};
</script>
