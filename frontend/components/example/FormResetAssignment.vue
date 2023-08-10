<template>
  <confirm-form
    title="Reset assignment"
    message="Are you sure you want to reset all the assignments?"
    @ok="$emit('reset')"
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
