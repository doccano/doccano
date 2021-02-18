<template>
  <v-stepper-content step="4">
    <v-card>
      <v-card-text class="pa-0">
        <h4 class="text-h6">Configure label mappings</h4>
        <p class="font-weight-regular body-1">
          Once you fetch the API response, you can convert the label into the defined one.
        </p>
        <label-mapping v-model="mapping" />
        <v-alert
          v-for="(error, index) in errorMessages"
          prominent
          type="error"
          :key="index"
        >
          <v-row align="center">
            <v-col class="grow">
              {{ error }}
            </v-col>
          </v-row>
        </v-alert>
      </v-card-text>
      <v-card-actions class="pa-0">
        <v-spacer />
        <v-btn
          text
          class="text-capitalize"
          @click="$emit('prev')"
        >
          Prev
        </v-btn>
        <v-btn
          v-show="!isPassed"
          color="primary"
          class="text-capitalize"
          @click="$emit('onTest')"
        >
          Test
        </v-btn>
        <v-btn
          v-show="isPassed"
          color="primary"
          class="text-capitalize"
          @click="$emit('next')"
        >
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
    }
  },

  computed: {
    mapping: {
      get() {
        return this.value
      },
      set(newVal) {
        this.$emit('input', newVal)
      }
    }
  }
})
</script>
