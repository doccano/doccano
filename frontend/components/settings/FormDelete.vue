<template>
  <base-card
    title="Delete Settings"
    :agree-text="$t('generic.yes')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('remove')"
    @cancel="$emit('cancel')"
  >
    <template #content>
      Are you sure you want to delete the following settings?
      <v-list dense>
        <v-list-item v-for="(item, i) in selected" :key="i">
          <v-list-item-content>
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </base-card>
</template>

<script>
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    selected: {
      type: Array,
      default: () => []
    }
  }
})
</script>