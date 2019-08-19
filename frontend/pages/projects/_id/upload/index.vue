<template>
  <v-content>
    <v-container
      fluid
      fill-height
    >
      <v-layout>
        <v-flex>
          <v-form
            ref="form"
            lazy-validation
          >
            <v-card>
              <v-card flat>
                <v-card-title>
                  Objective
                </v-card-title>
                <v-card-text>
                  <v-radio-group v-model="selectedTask">
                    <v-radio
                      v-for="(task, i) in tasks"
                      :key="i"
                      :label="task"
                      :value="task"
                    />
                  </v-radio-group>
                </v-card-text>
              </v-card>

              <v-card flat max-width="800">
                <v-card-title>
                  Import text items
                </v-card-title>
                <v-card-text>
                  <v-radio-group v-model="selectedFormat">
                    <v-radio
                      v-for="(format, i) in formats"
                      :key="i"
                      :label="format.text"
                      :value="format"
                    />
                  </v-radio-group>
                  <v-sheet color="black white--text" class="pa-3">
                    {{ selectedFormat }}
                  </v-sheet>
                </v-card-text>
              </v-card>

              <v-card flat max-width="500">
                <v-card-title>
                  Select file
                </v-card-title>
                <v-card-text>
                  <v-file-input :accept="acceptType" label="File input" />
                </v-card-text>
              </v-card>

              <v-card-actions>
                <v-btn>
                  Import Dataset
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-form>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
export default {
  layout: 'project',
  data() {
    return {
      selectedTask: null,
      selectedFormat: null,
      tasks: [
        'Text Classification',
        'Sequence Labeling',
        'Seq2seq'
      ],
      formats: [
        {
          type: 'csv',
          text: 'Upload a CSV file from your computer',
          accept: '.csv'
        },
        {
          type: 'plain',
          text: 'Upload text items from your computer',
          accept: '.txt'
        },
        {
          type: 'json',
          text: 'Upload a JSON file from your computer',
          accept: '.json,.jsonl'
        }
      ]
    }
  },
  computed: {
    acceptType() {
      if (this.selectedFormat) {
        return this.selectedFormat.accept
      } else {
        return '.txt,.csv,.json,.jsonl'
      }
    }
  },
  methods: {
  }
}
</script>

<style scoped>
body pre {
  color: white;
}
</style>
