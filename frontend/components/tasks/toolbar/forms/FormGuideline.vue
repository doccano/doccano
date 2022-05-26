<template>
  <base-card
    :title="$t('annotation.guidelinePopupTitle')"
    :cancel-text="$t('generic.close')"
    @cancel="close"
  >
    <template #content>
      <viewer :initial-value="guidelineText" />
    </template>
  </base-card>
</template>

<script>
import 'tui-editor/dist/tui-editor-contents.css'
import 'highlight.js/styles/github.css'
import { Viewer } from '@toast-ui/vue-editor'
import BaseCard from '@/components/utils/BaseCard'
import '@/assets/style/editor.css'

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
      this.$emit('click:close')
    }
  }
}
</script>
