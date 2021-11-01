<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <v-btn
        icon
        v-on="on"
        @click="$emit('click:review')"
      >
        <v-icon v-if="isReviewd">
          mdi-check
        </v-icon>
        <v-icon v-else>
          mdi-close
        </v-icon>
      </v-btn>
    </template>
    <span v-if="isReviewd">{{ $t('annotation.checkedTooltip') }}</span>
    <span v-else>{{ $t('annotation.notCheckedTooltip') }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    isReviewd: {
      type: Boolean,
      default: false,
      required: true
    }
  }
})
</script>
