<template>
  <editor
    v-model="editorText"
    preview-style="vertical"
    height="inherit"
    @change="onEditorChange"
  />
</template>

<script>
import 'tui-editor/dist/tui-editor.css'
import 'tui-editor/dist/tui-editor-contents.css'
import 'codemirror/lib/codemirror.css'
import { Editor } from '@toast-ui/vue-editor'
import { mapState, mapActions } from 'vuex'

export default {
  layout: 'project',
  components: {
    Editor
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      editorText: ''
    }
  },

  computed: {
    ...mapState('projects', ['current'])
  },

  async created() {
    await this.setCurrentProject(this.$route.params.id)
    this.editorText = this.current.guideline
  },

  methods: {
    ...mapActions('projects', ['setCurrentProject', 'updateCurrentProject']),

    onEditorChange() {
      const data = {
        projectId: this.$route.params.id,
        guideline: this.editorText
      }
      this.updateCurrentProject(data)
    }
  }
}
</script>

<style>
.te-md-container .CodeMirror, .tui-editor-contents {
  font-size: 20px;
}
</style>
