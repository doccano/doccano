<template>
  <confirm-form
    :title="$t('dataset.deleteDocumentsTitle')"
    :message="$t('dataset.deleteDocumentsMessage', { number: selected.length })"
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
    },
    itemKey: {
      type: String,
      default: 'text'
    }
  }
})
</script>
