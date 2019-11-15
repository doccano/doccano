<template>
  <editor
    v-if="current"
    v-model="editorText"
    preview-style="vertical"
    height="inherit"
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

  middleware: ['check-auth', 'auth', 'check-admin'],

  components: {
    Editor
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  computed: {
    ...mapState('projects', ['current']),

    editorText: {
      get() {
        return this.current.guideline
      },
      set(value) {
        const data = {
          projectId: this.$route.params.id,
          guideline: value
        }
        this.updateCurrentProject(data)
      }
    }
  },

  async created() {
    await this.setCurrentProject(this.$route.params.id)
  },

  methods: {
    ...mapActions('projects', ['setCurrentProject', 'updateCurrentProject'])
  }
}
</script>

<style>
.te-md-container .CodeMirror, .tui-editor-contents {
  font-size: 20px;
}
</style>
