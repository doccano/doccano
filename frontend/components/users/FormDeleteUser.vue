<template>
  <base-card
    :title="$t('overview.deleteUserTitle')"
    :agree-text="$t('generic.yes')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('remove')"
    @cancel="$emit('cancel')"
  >
    <template #content>
      {{ $t('overview.deleteUserMessage') }}
      <v-list dense>
        <v-list-item v-for="(item, i) in selected" :key="i">
          <v-list-item-content>
            <v-list-item-title>{{ item.delete }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </base-card>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import User from '~/domain/models/user/user'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    selected: {
      type: Array as PropType<User[]>,
      default: () => []
    }
  }
})
</script>