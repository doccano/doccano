<template>
  <confirm-form
    title="Clear annotations"
    message="Are you sure you want to delete all annotations?"
    :button-true-text="$t('generic.yes')"
    :button-false-text="$t('generic.cancel')"
    @ok="$emit('click:ok')"
    @cancel="$emit('click:cancel')"
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
