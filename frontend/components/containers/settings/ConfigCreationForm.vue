<template>
  <v-stepper
    v-model="step.count"
  >
    <v-overlay :value="isLoading">
      <v-progress-circular indeterminate size="64" />
    </v-overlay>
    <config-header :step="step.count" />
    <config-template-name
      v-model="templateConfig"
      @next="step.next()"
    />
    <config-parameters
      v-if="templateConfig.model_attrs !== undefined"
      v-model="templateConfig.model_attrs"
      :is-passed="passTesting.parameter"
      :error-messages="errors"
      :response="response.parameter"
      @prev="step.prev()"
      @next="step.next()"
      @onTest="testParameters"
    />

    <config-template
      v-model="templateConfig.template"
      :is-passed="passTesting.template"
      :error-messages="errors"
      :response="response.parameter"
      :result="response.template"
      @prev="step.prev()"
      @next="step.next()"
      @onTest="testTemplate"
    />

    <config-label-mapping
      v-model="labelMapping"
      :error-messages="errors"
      :is-passed="passTesting.mapping"
      @prev="step.prev()"
      @next="saveConfig"
      @onTest="testMapping"
    />
  </v-stepper>
</template>

<script lang="ts">
import Vue from 'vue'
import { FromApiConfigItemListRepository } from '@/repositories/config/api'
import { ConfigApplicationService } from '@/services/application/config.service'
import { ConfigItem, Parameters } from '@/models/config/config-item-list'
import { StepCounter } from '@/models/stepper'
import ConfigHeader from './form/ConfigHeader.vue'
import ConfigTemplateName from './form/ConfigTemplateName.vue'
import ConfigTemplate from './form/ConfigTemplate.vue'
import ConfigParameters from './form/ConfigParameters.vue'
import ConfigLabelMapping from './form/ConfigLabelMapping.vue'

export default Vue.extend({
  components: {
    ConfigHeader,
    ConfigTemplate,
    ConfigTemplateName,
    ConfigParameters,
    ConfigLabelMapping
  },

  data() {
    return {
      errors: [] as string[],
      isLoading: false,
      passTesting: {
        parameter: false,
        template: false,
        mapping: false
      },
      step: new StepCounter(1, 4),
      templateConfig: {},
      labelMapping: [],
      response: {
        parameter: [],
        template: [],
        mapping: []
      }
    }
  },

  computed: {
    configService(): ConfigApplicationService{
      const repository = new FromApiConfigItemListRepository()
      const service = new ConfigApplicationService(repository)
      return service
    }
  },

  watch: {
    templateConfig: {
      handler() {
        // this.passTesting = false
      },
      deep: true
    }
  },

  methods: {
    createConfig() {
      const payload = {
        // @ts-ignore
        modelName: this.templateConfig.model_name,
        // @ts-ignore
        modelAttrs: this.templateConfig.model_attrs,
        // @ts-ignore
        template: this.templateConfig.template,
        // @ts-ignore
        labelMapping: this.labelMapping
      }
      return ConfigItem.parseFromUI(payload)
    },
    testMapping() {
      const projectId = this.$route.params.id
      const item = this.createConfig()
      this.isLoading = true
      this.configService.testMapping(projectId, item, this.response.template)
        .then((value) => {
          this.passTesting.mapping = true
          // @ts-ignore
          this.response.mapping = value
        })
        .catch((error) => {
          this.errors = [error.message]
        })
        .finally(() => {
          this.isLoading = false
        })
    },
    testParameters(text: string) {
      // @ts-ignore
      const item = Parameters.parse(this.templateConfig.model_attrs)
      this.isLoading = true
      // @ts-ignore
      this.configService.testParameters(this.templateConfig.model_name, item, text)
        .then((value) => {
          // @ts-ignore
          this.response.parameter = value
          this.passTesting.parameter = true
        })
        .catch((error) => {
          this.errors = [error.message]
        })
        .finally(() => {
          this.isLoading = false
        })
    },
    testTemplate() {
      const projectId = this.$route.params.id
      this.isLoading = true
      this.errors = []
      // @ts-ignore
      this.configService.testTemplate(projectId, this.response.parameter, this.templateConfig.template)
        .then((value) => {
          // @ts-ignore
          this.response.template = value
          this.passTesting.template = true
        })
        .catch((error) => {
          this.errors = [error.message]
        })
        .finally(() => {
          this.isLoading = false
        })
    },
    saveConfig() {
      const projectId = this.$route.params.id
      const item = this.createConfig()
      this.isLoading = true
      this.configService.save(projectId, item)
        .then(() => {
          this.$emit('onCreate')
        })
        .finally(() => {
          this.isLoading = false
        })
    }
  }
})
</script>
