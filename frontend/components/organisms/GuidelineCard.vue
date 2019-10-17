<template>
  <v-card>
    <v-card-title
      class="headline grey lighten-2"
      primary-title
    >
      Annotation Guideline
    </v-card-title>

    <v-card-text>
      <viewer
        :value="guidelineText"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import 'tui-editor/dist/tui-editor-contents.css'
import 'highlight.js/styles/github.css'
import { Viewer } from '@toast-ui/vue-editor'

export default {
  components: {
    Viewer
  },

  props: {
    guidelineText: {
      type: String,
      default: '',
      required: true
    }
  }
}
</script>
