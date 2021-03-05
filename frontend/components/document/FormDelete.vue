<template>
  <confirm-form
    :items="selected"
    :title="$t('dataset.deleteDocumentsTitle')"
    :message="$t('dataset.deleteDocumentsMessage')"
    item-key="text"
    @ok="$emit('remove')"
    @cancel="$emit('cancel')"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import ConfirmForm from '@/components/organisms/utils/ConfirmForm.vue'

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
