<template>
  <v-stepper-content step="3">
    <v-card>
      <v-card-text class="pa-0">
        <h4 class="text-h6">Set mapping template</h4>
        <p class="font-weight-regular body-1">
          Now, you can successfuly fetch the API response. Next, you need to convert API response to
          doccano format with the mapping template.
        </p>
        <h4 class="text-h6">Response</h4>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>{{ JSON.stringify(response, null, 4) }}</pre>
        </v-sheet>
        <h4 class="text-h6">doccano format</h4>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>Text Classification</pre>
          <pre>[{ "label": "Cat" }, ...]</pre>
          <br />
          <pre>Sequence Labeling</pre>
          <pre>[{ "label": "Cat", "start_offset": 0, "end_offset": 5 }, ...]</pre>
          <br />
          <pre>Sequence to sequence</pre>
          <pre>[{ "text": "Cat" }, ...]</pre>
        </v-sheet>
        <h4 class="text-h6">Mapping template</h4>
        <p class="font-weight-regular body-1">
          You can set mapping template(<a href="https://jinja.palletsprojects.com/en/2.11.x/"
            >Jinja2</a
          >
          format) to convert API response to doccano format. In the template, you can refer to the
          API response by the
          <strong>input</strong> variable. If you want to know the Jinja2 notation, please refer to
          the site.
        </p>
        <v-textarea
          :value="value"
          outlined
          label="Mapping Template"
          @change="$emit('input', $event)"
        />
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
        <v-btn v-show="isPassed" color="primary" class="text-capitalize" @click="$emit('next')">
          Next
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-stepper-content>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    value: {
      type: String,
      default: '',
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
  }
})
</script>
