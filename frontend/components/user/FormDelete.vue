<template>
  <base-card
    :title="$t('generic.delete')"
    :agree-text="$t('generic.delete')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('remove')"
    @cancel="$emit('cancel')"
  >
    <template #content>
      {{ $t('user.deleteConfirm') }}
      <v-list dense>
        <v-list-item v-for="item in selected" :key="item.id">
          <v-list-item-content>
            <v-list-item-title>{{ item.username }}</v-list-item-title>
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
import { User } from '~/domain/models/user/user'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    selected: {
      type: Array as PropType<User[]>,
      default: () => [],
      required: true
    }
  }
})
</script>
