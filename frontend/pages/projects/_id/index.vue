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
            v-if="e6 === index + 1"
            class="mb-12"
            width="560"
            height="315"
          >
            <youtube
              ref="youtube"
              :video-id="item.videoId"
            />
          </v-card>
          <v-btn
            color="primary mt-5"
            @click="next"
          >
            Continue
          </v-btn>
          <v-btn
            class="mt-5"
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
        { title: 'Import a dataset', videoId: 'dA4ID1DSxCE' },
        { title: 'Create labels for this project', videoId: '1bSML270quU' },
        { title: 'Add members for collaborative work', videoId: 'NI09dcBz-qA' },
        { title: 'Define a guideline for the work', videoId: 'AvvX3Xs32nA' },
        { title: 'Annotate the dataset', videoId: 'F3XoSdyiMhA' },
        { title: 'View statistics', videoId: 'kfRpa0mNQMY' },
        { title: 'Export the dataset', videoId: 'Pfy_QcHEeQ4' }
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
