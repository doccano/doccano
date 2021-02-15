<template>
  <v-stepper
    v-model="step.count"
  >
    <v-stepper-header>
      <v-stepper-step
        :complete="step.count > 1"
        step="1"
      >
        Select a config template
      </v-stepper-step>
      <v-divider />
      <v-stepper-step
        :complete="step.count > 2"
        step="2"
      >
        Configure parameters
      </v-stepper-step>
      <v-divider />
      <v-stepper-step
        :complete="step.count > 3"
        step="3"
      >
        Test the config
      </v-stepper-step>
    </v-stepper-header>
    
    <v-card>
      <v-card-text class="pa-0">
        <v-stepper-content step="1">
          <h4 class="text-h6">Select a config template</h4>
          <p class="font-weight-regular body-1">
            You can select the template to create the auto-labeling configuration.
          </p>
          <v-select
            v-model="templateName"
            :items="templateNames"
            label="Select a config template"
            outlined
          />
        </v-stepper-content>

        <v-stepper-content step="2">
          <h4 class="text-h6">Set parameters</h4>
          <p class="font-weight-regular body-1">
            You can set parameters to fetch API response.
          </p>
          <template v-for="item in templateConfig.model_attrs">
            <v-text-field
              v-if="item.type === 'textField'"
              v-model="item.value"
              :label="item.name"
              outlined
              :key="item.name"
            />
            <v-select
              v-if="item.type === 'selectField'"
              v-model="item.value"
              :items="item.items"
              :label="item.name"
              outlined
              :key="item.name"
            />
          </template>

          <h4 class="text-h6">Set mapping template</h4>
          <p class="font-weight-regular body-1">
            You can set mapping template to convert API response to doccano format.
          </p>
          <v-textarea
            v-model="templateConfig.template"
            outlined
            label="Mapping Template"
          />

          <h4 class="text-h6">Configure label mappings</h4>
          <p class="font-weight-regular body-1">
            Once you fetch the API response, you can convert the label into the defined one.
          </p>
          <label-mapping v-model="templateConfig.label_mapping" />
        </v-stepper-content>

        <v-stepper-content step="3">
          <h4 class="text-h6">Test the defined config</h4>
          <p class="font-weight-regular body-1">
            Before saving the config, you need to test the defined config.
            Please input sample text and press the <strong>Test</strong> button.
          </p>
          <v-text-field
            v-model="sampleText"
            outlined
            label="Sample Text"
          />
        </v-stepper-content>
      </v-card-text>
      <v-card-actions class="me-4">
        <v-spacer />
          <v-btn
            v-show="step.hasPrev()"
            text
            class="text-capitalize"
            @click="step.prev()"
          >
            Prev
          </v-btn>
          <v-btn
            v-show="step.hasNext()"
            :disabled="disabled"
            color="primary"
            class="text-capitalize"
            @click="step.next()"
          >
            Next
          </v-btn>
          <v-btn
            v-show="step.isLast() && !passTesting"
            color="primary"
            class="text-capitalize"
            @click="testConfig"
          >
            Test
          </v-btn>
          <v-btn
            v-show="step.isLast() && passTesting"
            color="success"
            class="text-capitalize"
            @click="saveConfig"
          >
            Save
          </v-btn>
      </v-card-actions>
    </v-card>
  </v-stepper>
</template>

<script lang="ts">
import Vue from 'vue'
import { FromApiTemplateRepository } from '@/repositories/template/api'
import { FromApiConfigItemListRepository } from '@/repositories/config/api'
import { TemplateApplicationService } from '@/services/application/template.service'
import { ConfigApplicationService } from '@/services/application/config.service'
import { ConfigTemplateItem } from '@/models/config/config-template'
import { ConfigItem } from '@/models/config/config-item-list'
import { StepCounter } from '@/models/stepper'
import LabelMapping from '@/components/containers/settings/LabelMapping.vue'

export default Vue.extend({
  components: {
    LabelMapping
  },

  data() {
    return {
      passTesting: false,
      sampleText: '',
      step: new StepCounter(1, 3),
      templateName: null,
      templateConfig: {},
      templateNames: [] as string[]
    }
  },

  async created() {
    this.templateNames = await this.templateService.list(this.$route.params.id)
  },

  watch: {
    async templateName(val) {
      const projectId = this.$route.params.id
      const response: ConfigTemplateItem = await this.templateService.find(projectId, val)
      this.templateConfig = response.toObject()
    }
  },

  computed: {
    disabled(): boolean {
      return this.step.isFirst() && this.templateName === null
    },
    templateService(): TemplateApplicationService {
      const repository = new FromApiTemplateRepository()
      const service = new TemplateApplicationService(repository)
      return service
    },
    configService(): ConfigApplicationService{
      const repository = new FromApiConfigItemListRepository()
      const service = new ConfigApplicationService(repository)
      return service
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
        labelMapping: this.templateConfig.label_mapping
      }
      return ConfigItem.parseFromUI(payload)
    },
    testConfig() {
      const projectId = this.$route.params.id
      const item = this.createConfig()
      this.configService.testConfig(projectId, item, this.sampleText)
        .then(value => {
          this.passTesting = value.valid
        })
    },
    saveConfig() {
      const projectId = this.$route.params.id
      const item = this.createConfig()
      this.configService.save(projectId, item)
        .then(item => {
          this.$emit('onCreate')
        })
    }
  }
})
</script>
