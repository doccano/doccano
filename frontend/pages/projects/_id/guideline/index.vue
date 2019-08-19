<template>
  <v-content>
    <v-container
      fluid
      fill-height
    >
      <v-layout
        justify-center
      >
        <v-flex fill-height>
          <editor
            v-model="editorText"
            :options="editorOptions"
            :visible="editorVisible"
            preview-style="vertical"
            height="inherit"
          />
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import 'tui-editor/dist/tui-editor.css'
import 'tui-editor/dist/tui-editor-contents.css'
import 'codemirror/lib/codemirror.css'
import { Editor } from '@toast-ui/vue-editor'

export default {
  layout: 'project',
  components: {
    Editor
  },
  data() {
    return {
      editorText: 'Write annotation guideline.',
      editorOptions: {
      },
      editorVisible: true
    }
  }
}
</script>

<style>
.te-md-container .CodeMirror, .tui-editor-contents {
  font-size: 20px;
}
</style>
