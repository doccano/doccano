<template>
  <v-card>
    <v-card-title>
      Welcome to doccano!
    </v-card-title>
    <v-stepper
      v-model="e6"
      vertical
      non-linear
    >
      <div
        v-for="(item, index) in items"
        :key="index"
      >
        <v-stepper-step
          :complete="e6 > index + 1"
          :step="index + 1"
          editable
        >
          {{ item.title }}
        </v-stepper-step>
        <v-stepper-content :step="index + 1">
          <v-card
            color="grey lighten-1"
            class="mb-12"
            height="200px"
          />
          <v-btn
            color="primary"
            @click="next"
          >
            Continue
          </v-btn>
          <v-btn
            text
            @click="prev"
          >
            Cancel
          </v-btn>
        </v-stepper-content>
      </div>
    </v-stepper>
  </v-card>
</template>

<script>
export default {
  layout: 'project',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      e6: 1,
      items: [
        { title: 'Import a dataset' },
        { title: 'Create labels for this project' },
        { title: 'Add members for collaborative work' },
        { title: 'Define a guideline for the work' },
        { title: 'Annotate the dataset' },
        { title: 'View statistics' },
        { title: 'Export the dataset' }
      ]
    }
  },

  methods: {
    next() {
      this.e6 = Math.max(1, (this.e6 + 1) % (this.items.length + 1))
    },
    prev() {
      this.e6 = Math.max(1, this.e6 - 1)
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
