<template>
  <confirm-form
    :title="$t('dataset.deleteBulkDocumentsTitle')"
    :message="$t('dataset.deleteBulkDocumentsMessage')"
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
  }
})
</script>
