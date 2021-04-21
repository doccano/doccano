<template>
  <editor
    v-model="project.guideline"
    preview-style="vertical"
    height="inherit"
    :options="editorOptions"
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
      project: {}
    }
  },

  watch: {
    'project.guideline'() {
      this.updateProject()
    }
  },

  async created() {
    const projectId = this.$route.params.id
    this.project = await this.$services.project.findById(projectId)
  },

  methods: {
    updateProject: _.debounce(function() {
      this.$services.project.update(this.project)
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
