<template>
  <v-stepper-content step="4">
    <v-card>
      <v-card-text class="pa-0">
        <h4 class="text-h6">Configure label mappings</h4>
        <p class="font-weight-regular body-1">
          Once you fetch the API response, you need to convert the label in the response into the
          one which you defined at the label page.
        </p>
        <h4 class="text-h6">Response</h4>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>{{ JSON.stringify(response, null, 4) }}</pre>
        </v-sheet>
        <label-mapping v-model="mapping" />
        <v-alert v-for="(error, index) in errorMessages" :key="index" prominent type="error">
          <v-row align="center">
            <v-col class="grow">
              {{ error }}
            </v-col>
          </v-row>
        </v-alert>
        <h4 class="text-h6">Result</h4>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>{{ JSON.stringify(result, null, 4) }}</pre>
        </v-sheet>
      </v-card-text>
      <v-card-actions class="pa-0">
        <v-spacer />
        <v-btn text class="text-capitalize" @click="$emit('prev')"> Prev </v-btn>
        <v-btn v-show="!isPassed" color="primary" class="text-capitalize" @click="$emit('onTest')">
          Test
        </v-btn>
        <v-btn v-show="isPassed" color="success" class="text-capitalize" @click="$emit('next')">
          Finish
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-stepper-content>
</template>

<script lang="ts">
import Vue from 'vue'
import LabelMapping from './LabelMapping.vue'

export default Vue.extend({
  components: {
    LabelMapping
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
      type: [String, Object, Array],
      default: () => [],
      required: true
    },
    result: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  computed: {
    mapping: {
      get() {
        // @ts-ignore
        return this.value
      },
      set(newVal) {
        // @ts-ignore
        this.$emit('input', newVal)
      }
    }
  }
})
</script>
