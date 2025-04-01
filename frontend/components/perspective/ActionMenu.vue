<template>
  <action-menu :items="items" :text="$t('dataset.actions')" @create="$emit('create')" />
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiPencil } from '@mdi/js'
import ActionMenu from '~/components/utils/ActionMenu.vue'

export default Vue.extend({
  components: {
    ActionMenu
  },

  computed: {
    items() {
      const items = [
        {
          title: this.$t('Create Perspective'),
          icon: mdiPencil,
          event: 'create'
        }
      ]
      return items
    }
  }
})
</script>
