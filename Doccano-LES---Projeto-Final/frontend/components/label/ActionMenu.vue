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
import { mdiPencil, mdiUpload, mdiDownload } from '@mdi/js'
import ActionMenu from '~/components/utils/ActionMenu.vue'

export default Vue.extend({
  components: {
    ActionMenu
  },

  props: {
    addOnly: {
      type: Boolean,
      default: false
    }
  },

  computed: {
    items() {
      const items = [
        {
          title: this.$t('labels.createLabel'),
          icon: mdiPencil,
          event: 'create'
        }
      ]
      if (this.addOnly) {
        return items
      } else {
        return items.concat([
          {
            title: this.$t('labels.importLabels'),
            icon: mdiUpload,
            event: 'upload'
          },
          {
            title: this.$t('labels.exportLabels'),
            icon: mdiDownload,
            event: 'download'
          }
        ])
      }
    }
  }
})
</script>
