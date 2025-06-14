<template>
  <v-stepper v-model="step.count">
    <v-overlay :value="isLoading">
      <v-progress-circular indeterminate size="64" />
    </v-overlay>
    <config-header :step="step.count" />
    <config-template-name v-model="fields" @next="step.next()" />
    <config-parameters
      v-if="fields.modelAttrs !== undefined"
      v-model="fields.modelAttrs"
      :is-passed="passTesting.parameter"
      :error-messages="errors"
      :response="response.parameter"
      @prev="step.prev()"
      @next="step.next()"
      @onTest="testParameters"
    />

    <config-template
      v-model="fields.template"
      :is-passed="passTesting.template"
      :error-messages="errors"
      :response="response.parameter"
      :result="response.template"
      @prev="step.prev()"
      @next="step.next()"
      @onTest="testTemplate"
    />

    <config-label-mapping
      v-model="fields.labelMapping"
      :is-passed="passTesting.mapping"
      :error-messages="errors"
      :response="response.template"
      :result="response.mapping"
      @prev="step.prev()"
      @next="saveConfig"
      @onTest="testMapping"
    />
  </v-stepper>
</template>

<script lang="ts">
import Vue from 'vue'
import ConfigHeader from './form/ConfigHeader.vue'
import ConfigLabelMapping from './form/ConfigLabelMapping.vue'
import ConfigParameters from './form/ConfigParameters.vue'
import ConfigTemplate from './form/ConfigTemplate.vue'
import ConfigTemplateName from './form/ConfigTemplateName.vue'
import { StepCounter } from '@/domain/models/utils/stepper'
import { ConfigItem, Fields } from '@/domain/models/autoLabeling/config'

export default Vue.extend({
  components: {
    ConfigHeader,
    ConfigLabelMapping,
    ConfigParameters,
    ConfigTemplate,
    ConfigTemplateName
  },

  data() {
    return {
      config: {} as ConfigItem,
      errors: [] as string[],
      fields: {} as Fields,
      isLoading: false,
      step: new StepCounter(),
      passTesting: {
        parameter: false,
        template: false,
        mapping: false
      },
      response: {
        parameter: [],
        template: [],
        mapping: []
      }
    }
  },

  watch: {
    'fields.modelName'() {
      this.passTesting = { parameter: false, template: false, mapping: false }
    },
    'fields.modelAttrs': {
      handler() {
        this.passTesting = {
          parameter: false,
          template: false,
          mapping: false
        }
      },
      deep: true
    },
    'fields.template'() {
      this.passTesting = { parameter: true, template: false, mapping: false }
    },
    'fields.labelMapping': {
      handler() {
        this.passTesting = { parameter: true, template: true, mapping: false }
      },
      deep: true
    }
  },

  methods: {
    testConfig(promise: Promise<any>, key: 'parameter' | 'template' | 'mapping') {
      this.isLoading = true
      promise
        .then((value) => {
          this.response[key] = value
          this.passTesting[key] = true
          this.errors = []
        })
        .catch((error) => {
          this.errors = [error.response.data]
        })
        .finally(() => {
          this.isLoading = false
        })
    },
    testParameters(text: string) {
      const projectId = this.$route.params.id
      const item = ConfigItem.parseFromUI(this.fields)
      const promise = this.$repositories.config.testParameters(projectId, item, text)
      this.testConfig(promise, 'parameter')
    },
    testTemplate() {
      const projectId = this.$route.params.id
      const item = ConfigItem.parseFromUI(this.fields)
      const promise = this.$repositories.config.testTemplate(
        projectId,
        this.response.parameter,
        item
      )
      this.testConfig(promise, 'template')
    },
    testMapping() {
      const projectId = this.$route.params.id
      const item = ConfigItem.parseFromUI(this.fields)
      const promise = this.$repositories.config.testMapping(projectId, item, this.response.template)
      this.testConfig(promise, 'mapping')
    },
    saveConfig() {
      const projectId = this.$route.params.id
      const item = ConfigItem.parseFromUI(this.fields)
      this.isLoading = true
      this.$repositories.config
        .create(projectId, item)
        .then(() => {
          this.step.first()
          this.$emit('onCreate')
        })
        .finally(() => {
          this.isLoading = false
        })
    }
  }
})
</script>
