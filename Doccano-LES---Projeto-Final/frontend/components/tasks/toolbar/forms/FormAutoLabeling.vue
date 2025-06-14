<template>
  <base-card title="Settings" :cancel-text="$t('generic.close')" @cancel="$emit('click:cancel')">
    <template #content>
      <h3>Auto Labeling</h3>
      <p>
        The auto labeling allows users to annotate data automatically. It enables them to speed up
        annotating data. You only have to correct labels which are mislabeled by the system and
        annotate labels which aren’t labeled by it.
      </p>
      <p>
        Notice that you can't use this feature unless the project administrators configure the auto
        labeling. Also, depending on the configuration, it will take some cost for the
        administrators(e.g. In the case of configuring some paid service like AWS or GCP).
      </p>
      <v-switch
        :value="isEnabled"
        :error-messages="errorMessage"
        @change="$emit('input', $event)"
      />
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    isEnabled: {
      type: Boolean,
      default: false,
      required: true
    },
    errorMessage: {
      type: String,
      default: '',
      required: true
    }
  }
})
</script>
