<template>
  <v-stepper-content step="2">
    <v-card>
      <v-card-text class="pa-0">
        <v-form>
          <h4 class="text-h6">Set parameters</h4>
          <p class="font-weight-regular body-1">You can set parameters to fetch API response.</p>
          <template v-for="item in value">
            <v-text-field
              v-if="item.type === 'textField'"
              :key="item.name"
              v-model="item.value"
              :label="item.name"
              outlined
            />
            <v-select
              v-if="item.type === 'selectField'"
              :key="item.name"
              v-model="item.value"
              :items="item.items"
              :label="item.name"
              outlined
            />
            <object-field
              v-if="item.type === 'objectField'"
              :key="item.name"
              v-model="item.value"
              :title="item.name"
            />
          </template>
          <h4 class="text-h6">Test the parameters</h4>
          <p class="font-weight-regular body-1">
            Before proceeding, you need to test the parameters whether they can fetch API response.
            Please input sample text and press the
            <strong>Test</strong> button.
          </p>
          <v-text-field
            v-if="project.isTextProject"
            v-model="payload"
            outlined
            label="Sample Text"
          />
          <file-field v-else v-model="payload" />
          <v-alert v-for="(error, index) in errorMessages" :key="index" prominent type="error">
            <v-row align="center">
              <v-col class="grow">
                {{ error }}
              </v-col>
            </v-row>
          </v-alert>
          <h4 class="text-h6">Response</h4>
          <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
            <pre>{{ JSON.stringify(response, null, 4) }}</pre>
          </v-sheet>
        </v-form>
      </v-card-text>
      <v-card-actions class="pa-0">
        <v-spacer />
        <v-btn text class="text-capitalize" @click="$emit('prev')"> Prev </v-btn>
        <v-btn
          v-show="!isPassed"
          color="primary"
          class="text-capitalize"
          @click="$emit('onTest', payload)"
        >
          Test
        </v-btn>
        <v-btn v-show="isPassed" color="primary" class="text-capitalize" @click="$emit('next')">
          Next
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-stepper-content>
</template>

<script lang="ts">
import Vue from 'vue'
import FileField from './FileField.vue'
import ObjectField from './ObjectField.vue'
import { Project } from '~/domain/models/project/project'

export default Vue.extend({
  components: {
    ObjectField,
    FileField
  },

  props: {
    value: {
      type: Array,
      default: () => [],
      required: true
    },
    errorMessages: {
      type: Array,
      default: () => [],
      required: true
    },
    isPassed: {
      type: Boolean,
      default: false,
      required: true
    },
    response: {
      type: [String, Array, Object],
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      payload: '',
      project: {} as Project
    }
  },

  async created() {
    this.project = await this.$services.project.findById(this.$route.params.id)
  }
})
</script>
