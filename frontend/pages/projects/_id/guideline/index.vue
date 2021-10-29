<template>
  <editor
    :initialValue="project.guideline"
    :options="editorOptions"
    preview-style="vertical"
    height="inherit"
    ref="toastuiEditor"
    @change="updateProject"
  />
</template>

<script>
import _ from 'lodash'
import 'tui-editor/dist/tui-editor.css'
import 'tui-editor/dist/tui-editor-contents.css'
import 'codemirror/lib/codemirror.css'
import { Editor } from '@toast-ui/vue-editor'
import '@/assets/style/editor.css'

export default {
  layout: 'project',

  components: {
    Editor
  },

  data() {
    return {
      editorOptions: {
        language: this.$t('toastui.localeCode')
      },
      project: {},
      mounted: false,
    }
  },

  async mounted() {
    const projectId = this.$route.params.id
    this.project = await this.$services.project.findById(projectId)
    this.$refs.toastuiEditor.invoke('setMarkdown', this.project.guideline)
    this.mounted = true
  },

  methods: {
    updateProject: _.debounce(function() {
      if (this.mounted) {
        this.project.guideline = this.$refs.toastuiEditor.invoke('getMarkdown')
        this.$services.project.update(this.project)
      }
    }, 1000)
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>

<style>
.te-md-container .CodeMirror, .tui-editor-contents {
  font-size: 20px;
}
</style>
