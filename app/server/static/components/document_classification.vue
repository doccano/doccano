<template lang="pug">
extends ./annotation.pug

block annotation-area
  div.card
    header.card-header
      div.card-header-title.has-background-royalblue
        div.field.is-grouped.is-grouped-multiline
          div.control(v-for="label in labels")
            div.tags.has-addons
              a.tag.is-medium(
                v-shortkey.once="replaceNull(shortcutKey(label))"
                v-bind:style="{ \
                  color: label.text_color, \
                  backgroundColor: label.background_color \
                }"
                v-on:click="addLabel(label)"
                v-on:shortkey="addLabel(label)"
              ) {{ label.text }}
              span.tag.is-medium
                kbd {{ shortcutKey(label) | simpleShortcut }}

    div.card-content
      div.field.is-grouped.is-grouped-multiline
        div.control(v-for="annotation in annotations[pageNumber]")
          div.tags.has-addons(v-if="id2label[annotation.label]")
            span.tag.is-medium(
              v-bind:style="{ \
                color: id2label[annotation.label].text_color, \
                backgroundColor: id2label[annotation.label].background_color \
              }"
            ) {{ id2label[annotation.label].text }}
              button.delete.is-small(v-on:click="removeLabel(annotation)")

      hr
      div.content(v-if="docs[pageNumber]")
        span.text {{ docs[pageNumber].text }}
</template>

<style scoped>
hr {
  margin: 0.8rem 0;
}

.card-header-title {
  padding: 1.5rem;
}
</style>

<script>
import annotationMixin from './annotationMixin';
import HTTP from './http';
import { simpleShortcut } from './filter';

export default {
  filters: { simpleShortcut },

  mixins: [annotationMixin],

  methods: {
    getAnnotation(label) {
      return this.annotations[this.pageNumber].find(annotation => annotation.label === label.id);
    },

    async submit() {
      const state = this.getState();
      this.url = `docs?q=${this.searchQuery}&doc_annotations__isnull=${state}&offset=${this.offset}`;
      await this.search();
      this.pageNumber = 0;
    },

    async addLabel(label) {
      const annotation = this.getAnnotation(label);
      if (annotation) {
        this.removeLabel(annotation);
      } else {
        const docId = this.docs[this.pageNumber].id;
        const payload = {
          label: label.id,
        };
        await HTTP.post(`docs/${docId}/annotations`, payload).then((response) => {
          this.annotations[this.pageNumber].push(response.data);
        });
      }
    },
  },
};
</script>
