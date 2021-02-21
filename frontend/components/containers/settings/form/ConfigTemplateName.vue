<template>
  <v-stepper-content step="1">
    <v-card>
      <v-card-text class="pa-0">
        <v-form v-model="valid">
          <h4 class="text-h6">Select a config template</h4>
          <p class="font-weight-regular body-1">
            You can select the template to create the auto-labeling configuration.
          </p>
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
        <v-btn
          :disabled="!valid"
          color="primary"
          class="text-capitalize"
          @click="$emit('next')"
        >
          Next
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-stepper-content>
</template>

<script lang="ts">
import Vue from 'vue'
import { FromApiTemplateRepository } from '@/repositories/template/api'
import { TemplateApplicationService } from '@/services/application/template.service'
import { ConfigTemplateItem } from '@/models/config/config-template'
import { templateNameRules } from '@/rules/index'

export default Vue.extend({
  data() {
    return {
      templateName: null,
      templateNames: [] as string[],
      templateNameRules,
      valid: false
    }
  },

  computed: {
    templateService(): TemplateApplicationService {
      const repository = new FromApiTemplateRepository()
      const service = new TemplateApplicationService(repository)
      return service
    }
  },

  watch: {
    async templateName(val) {
      const projectId = this.$route.params.id
      const response: ConfigTemplateItem = await this.templateService.find(projectId, val)
      this.$emit('input', response.toObject())
    },
  },

  async created() {
    this.templateNames = await this.templateService.list(this.$route.params.id)
  }
})
</script>
