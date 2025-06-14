<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn
        v-shortkey.once="['enter']"
        icon
        v-on="on"
        @shortkey="$emit('click:review')"
        @click="$emit('click:review')"
      >
        <v-icon v-if="isReviewd">
          {{ mdiCheck }}
        </v-icon>
        <v-icon v-else>
          {{ mdiClose }}
        </v-icon>
      </v-btn>
    </template>
    <span v-if="isReviewd">{{ $t('annotation.checkedTooltip') }}</span>
    <span v-else>{{ $t('annotation.notCheckedTooltip') }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiClose, mdiCheck } from '@mdi/js'

export default Vue.extend({
  props: {
    isReviewd: {
      type: Boolean,
      default: false,
      required: true
    }
  },

  data() {
    return {
      mdiClose,
      mdiCheck
    }
  }
})
</script>
