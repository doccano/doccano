<template>
  <v-card>
    <v-card-title>
      Welcome doccano!
    </v-card-title>
    <v-stepper v-model="e6" vertical non-linear>
      <v-stepper-step :complete="e6 > 1" step="1" editable>
        Import a dataset
      </v-stepper-step>
      <v-stepper-content step="1">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="e6 = 2">Continue</v-btn>
        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 2" step="2" editable>Create labels for this project</v-stepper-step>
      <v-stepper-content step="2">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="e6 = 3">Continue</v-btn>
        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 3" step="3" editable>Add members for collaborative work</v-stepper-step>
      <v-stepper-content step="3">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="e6 = 4">Continue</v-btn>
        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 4" step="4" editable>Define a guideline for the work</v-stepper-step>
      <v-stepper-content step="4">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="e6 = 5">Continue</v-btn>
        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 5" step="5" editable>Annotate the dataset</v-stepper-step>
      <v-stepper-content step="5">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="e6 = 6">Continue</v-btn>
        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 6" step="6" editable>View statistics</v-stepper-step>
      <v-stepper-content step="6">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="e6 = 7">Continue</v-btn>
        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 7" step="7" editable>Export the dataset</v-stepper-step>
      <v-stepper-content step="7">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="e6 = 1">Finish</v-btn>
        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

    </v-stepper>
  </v-card>
</template>

<script>
export default {
  layout: 'project',

  data() {
    return {
      e6: 1
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
