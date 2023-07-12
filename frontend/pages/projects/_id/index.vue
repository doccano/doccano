<template>
  <v-card>
    <v-card-title>
      {{ $t('projectHome.welcome') }}
    </v-card-title>
    <v-stepper v-model="e6" vertical non-linear>
      <div v-for="(item, index) in items" :key="index">
        <v-stepper-step :complete="e6 > index + 1" :step="index + 1" editable>
          {{ item.title }}
        </v-stepper-step>
        <v-stepper-content :step="index + 1">
          <v-card v-if="e6 === index + 1" class="mb-12" width="560" height="315">
            <youtube ref="youtube" :video-id="item.videoId" />
          </v-card>
          <v-btn color="primary mt-5" @click="next">
            {{ $t('generic.continue') }}
          </v-btn>
          <v-btn class="mt-5" text @click="prev">
            {{ $t('generic.cancel') }}
          </v-btn>
        </v-stepper-content>
      </div>
    </v-stepper>
  </v-card>
</template>

<script>
export default {
  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      e6: 1,
      items: [
        { title: this.$t('projectHome.importData'), videoId: 'dA4ID1DSxCE' },
        { title: this.$t('projectHome.createLabels'), videoId: '1bSML270quU' },
        { title: this.$t('projectHome.addMembers'), videoId: 'NI09dcBz-qA' },
        {
          title: this.$t('projectHome.defineGuideline'),
          videoId: 'AvvX3Xs32nA'
        },
        {
          title: this.$t('projectHome.annotateDataset'),
          videoId: 'F3XoSdyiMhA'
        },
        {
          title: this.$t('projectHome.viewStatistics'),
          videoId: 'kfRpa0mNQMY'
        },
        { title: this.$t('projectHome.exportDataset'), videoId: 'Pfy_QcHEeQ4' }
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
  }
}
</script>
