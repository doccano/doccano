<template>
  <confirm-form
    :items="selected"
    title="Delete Label"
    :message="$t('labels.deleteMessage')"
    item-key="text"
    @ok="$emit('remove')"
    @cancel="$emit('cancel')"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import ConfirmForm from '@/components/utils/ConfirmForm.vue'

export default Vue.extend({
  components: {
    ConfirmForm
  },

  props: {
    selected: {
      type: Array,
      default: () => []
    }
  }
})
</script>
