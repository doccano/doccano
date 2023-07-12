<template>
  <editor
    ref="toastuiEditor"
    :initial-value="project.guideline"
    :options="editorOptions"
    preview-style="vertical"
    height="inherit"
    @change="updateProject"
  />
</template>

<script>
import '@/assets/style/editor.css'
import { Editor } from '@toast-ui/vue-editor'
import 'codemirror/lib/codemirror.css'
import _ from 'lodash'
import 'tui-editor/dist/tui-editor-contents.css'
import 'tui-editor/dist/tui-editor.css'

export default {
  components: {
    Editor
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      editorOptions: {
        language: this.$t('toastui.localeCode')
      },
      project: {},
      mounted: false
    }
  },

  async mounted() {
    const projectId = this.$route.params.id
    this.project = await this.$services.project.findById(projectId)
    this.$refs.toastuiEditor.invoke('setMarkdown', this.project.guideline)
    this.mounted = true
  },

  methods: {
    updateProject: _.debounce(function () {
      if (this.mounted) {
        this.project.guideline = this.$refs.toastuiEditor.invoke('getMarkdown')
        this.$services.project.update(this.$route.params.id, this.project)
      }
    }, 1000)
  }
}
</script>

<style>
.te-md-container .CodeMirror,
.tui-editor-contents {
  font-size: 20px;
}
</style>
