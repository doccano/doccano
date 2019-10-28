<template>
  <base-modal
    text="Create"
    :is-create="true"
  >
    <template v-slot="slotProps">
      <label-creation-form
        :create-label="createLabel"
        @close="slotProps.close"
      />
    </template>
  </base-modal>
</template>

<script>
import { mapActions } from 'vuex'
import BaseModal from '@/components/molecules/BaseModal'
import LabelCreationForm from '@/components/organisms/labels/LabelCreationForm'

export default {
  components: {
    BaseModal,
    LabelCreationForm
  },

  methods: {
    ...mapActions('labels', ['createLabel'])
  }
}
</script>
