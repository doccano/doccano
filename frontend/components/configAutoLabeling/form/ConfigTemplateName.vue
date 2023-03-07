<template>
  <v-stepper-content step="1">
    <v-card>
      <v-card-text class="pa-0">
        <v-form ref="form" v-model="valid">
          <h4 class="text-h6">Select a config template</h4>
          <p class="font-weight-regular body-1">
            You can select the template to create the auto-labeling configuration.{{ valid }}
          </p>
          <v-select v-model="selectedTask" :items="taskNames" label="Select a task name" outlined />
          <v-select
            v-model="templateName"
            :items="templateNames"
            :rules="templateNameRules()"
            label="Select a config template"
            outlined
          />
        </v-form>
      </v-card-text>
      <v-card-actions class="pa-0">
        <v-spacer />
        <v-btn :disabled="!valid" color="primary" class="text-capitalize" @click="$emit('next')">
          Next
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-stepper-content>
</template>

<script lang="ts">
import Vue from 'vue'
import { templateNameRules } from '@/rules/index'
import { Project } from '~/domain/models/project/project'

export default Vue.extend({
  data() {
    return {
      project: {} as Project,
      selectedTask: '',
      templateName: null,
      templateNames: [] as string[],
      templateNameRules,
      valid: false
    }
  },

  computed: {
    projectId() {
      return this.$route.params.id
    },

    taskNames(): string[] {
      return this.project.taskNames
    },

    taskType(): string {
      return {
        DocumentClassification: 'Category',
        SequenceLabeling: 'Span',
        Seq2seq: 'Text',
        ImageClassification: 'Category',
        Speech2text: 'Text'
      }[this.selectedTask]!
    }
  },

  watch: {
    async templateName(val) {
      if (val) {
        const response = await this.$repositories.template.find(this.projectId, val)
        const field = response.toObject()
        field.taskType = this.taskType
        this.$emit('input', field)
      }
    },

    async selectedTask() {
      this.templateName = null
      await this.fetchTemplateNames()
      // @ts-ignore
      this.$refs.form.resetValidation()
    }
  },

  async created() {
    this.project = await this.$services.project.findById(this.projectId)
    this.selectedTask = this.taskNames[0]
    await this.fetchTemplateNames()
  },

  methods: {
    async fetchTemplateNames() {
      this.templateNames = await this.$repositories.template.list(this.projectId, this.selectedTask)
    }
  }
})
</script>
