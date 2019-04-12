<template lang="pug">
extends ../annotation.pug

block annotation-area
  div.card
    header.card-header
      div.card-header-title.has-background-royalblue(style="padding:1.5rem;")
        div.field.is-grouped.is-grouped-multiline
          div.control(v-for="label in labels")
            div.tags.has-addons
              a.tag.is-medium(
                :style="{ \
                  color: label.text_color, \
                  backgroundColor: label.background_color \
                }",
                @click="annotate(label.id)",
                v-shortkey.once="[ label.shortcut ]",
                @shortkey="annotate(label.id)"
              ) {{ label.text }}
              span.tag.is-medium {{ label.shortcut }}

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
