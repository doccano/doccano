<template>
  <base-card
    title="Annotation Guideline"
    cancel-text="Close"
    @cancel="close"
  >
    <template #content>
      <viewer
        :value="guidelineText"
      />
    </template>
  </base-card>
</template>

<script>
import 'tui-editor/dist/tui-editor-contents.css'
import 'highlight.js/styles/github.css'
import { Viewer } from '@toast-ui/vue-editor'
import BaseCard from '@/components/molecules/BaseCard'

export default {
  components: {
    Viewer,
    BaseCard
  },

  props: {
    guidelineText: {
      type: String,
      default: '',
      required: true
    }
  },

  methods: {
    close() {
      this.$emit('close')
    }
  }
}
</script>
