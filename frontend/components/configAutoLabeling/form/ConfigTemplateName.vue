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
    projectId() {
      return this.$route.params.id
    }
  },

  watch: {
    async templateName(val) {
      const response = await this.$services.template.find(this.projectId, val)
      this.$emit('input', response.toObject())
    },
  },

  async created() {
    this.templateNames = await this.$services.template.list(this.projectId)
  }
})
</script>
