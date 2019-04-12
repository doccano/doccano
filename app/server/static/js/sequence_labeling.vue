<template lang="pug">
extends ./annotation.pug

block annotation-area
  div.card
    header.card-header
      div.card-header-title.has-background-royalblue(style="padding: 1.5rem;")
        div.field.is-grouped.is-grouped-multiline
          div.control(v-for="label in labels")
            div.tags.has-addons
              a.tag.is-medium(
                :style="{ \
                  color: label.text_color, \
                  backgroundColor: label.background_color \
                }",
                @click="annotate(label.id)",
                v-shortkey.once="replaceNull(shortcutKey(label))",
                @shortkey="annotate(label.id)"
              ) {{ label.text }}
              span.tag.is-medium
                kbd {{ shortcutKey(label) | simpleShortcut }}

    div.card-content
      div.content(v-if="docs[pageNumber] && annotations[pageNumber]")
        annotator(
          ref="annotator",
          :labels="labels",
          :entity-positions="annotations[pageNumber]",
          :text="docs[pageNumber].text",
          @remove-label="removeLabel",
          @add-label="addLabel"
        )
</template>

<script>
import annotationMixin from './mixin';
import Annotator from './annotator.vue';
import HTTP from './http';
import { simpleShortcut } from './filter';

export default {
  filters: { simpleShortcut },

  components: { Annotator },

  mixins: [annotationMixin],

  methods: {
    annotate(labelId) {
      this.$refs.annotator.addLabel(labelId);
    },

    addLabel(annotation) {
      const docId = this.docs[this.pageNumber].id;
      HTTP.post(`docs/${docId}/annotations`, annotation).then((response) => {
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
