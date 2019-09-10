<template>
  <v-navigation-drawer
    :value="drawer"
    app
    clipped
    right
  >
    <v-list dense>
      <v-list-group
        sub-group
        value="true"
      >
        <template v-slot:activator>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                Progress
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
        <v-list-item class="pl-4">
          <v-list-item-content>
            <v-list-item-title>
              <v-progress-linear
                :value="progress"
                height="25"
                rounded
              >
                <strong>{{ Math.ceil(progress) }}%</strong>
              </v-progress-linear>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-group>

      <v-list-group
        sub-group
        value="true"
      >
        <template v-slot:activator>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                Labels
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
        <v-list-item
          v-for="(label, i) in labels"
          :key="i"
          class="pl-4"
        >
          <v-list-item-content>
            <v-list-item-title>
              <v-chip
                :color="label.color"
                text-color="white"
              >
                <v-avatar left>
                  <span class="white--text">{{ label.shortcut }}</span>
                </v-avatar>
                {{ label.name }}
              </v-chip>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-group>

      <v-list-item @click="showMetadata = true">
        <v-list-item-action>
          <v-icon>mdi-file-document-box</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            Show metadata
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item @click="showGuideline = true">
        <v-list-item-action>
          <v-icon>mdi-text-subject</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            Show guideline
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-dialog
      v-model="showMetadata"
      width="800"
    >
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          Metadata
        </v-card-title>

        <v-card-text>
          <v-sheet>
            <pre>{{ prettyJson }}</pre>
          </v-sheet>
        </v-card-text>

        <v-divider />

        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            text
            @click="showMetadata = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="showGuideline"
      width="800"
    >
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

        <v-divider />

        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            text
            @click="showGuideline = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-navigation-drawer>
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
    labels: {
      type: Array,
      default: () => ([]),
      required: true
    },
    progress: {
      type: Number,
      default: 0,
      required: true
    },
    metadata: {
      type: String,
      default: '{}',
      required: true
    },
    guidelineText: {
      type: String,
      default: '# This is Viewer.\n Hello World.'
    }
  },

  data: () => ({
    showMetadata: false,
    showGuideline: false
  }),

  computed: {
    drawer() {
      return this.$store.state.sidebar.drawer
    },
    prettyJson() {
      const data = JSON.parse(this.metadata)
      const pretty = JSON.stringify(data, null, 4)
      return pretty
    }
  }
}
</script>
