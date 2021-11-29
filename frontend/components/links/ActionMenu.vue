<template>
  <action-menu
    :items="items"
    :text="$t('dataset.actions')"
    @create="$emit('create')"
    @upload="$emit('upload')"
    @download="$emit('download')"
  />
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
        return [
        {
          title: this.$t('links.createLink'),
          icon: mdiPencil,
          event: 'create'
        }
      ]
    }
  }
})
</script>
