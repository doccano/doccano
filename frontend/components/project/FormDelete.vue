<template>
  <base-card
    :title="$t('overview.deleteProjectTitle')"
    :agree-text="$t('generic.yes')"
    :cancel-text="$t('generic.cancel')"
    @agree="$emit('remove')"
    @cancel="$emit('cancel')"
  >
    <template #content>
      {{ $t('overview.deleteProjectMessage') }}
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

<script lang="ts">
import Vue, { PropType } from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { ProjectDTO } from '~/services/application/project/projectData'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    selected: {
      type: Array as PropType<ProjectDTO[]>,
      default: () => []
    }
  }
})
</script>
