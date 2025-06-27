<template>
  <v-card>
    <v-card-title class="headline">{{ $t('generic.deleteConfirm') }}</v-card-title>
    <v-card-text>
      {{ $tc('group.confirmDelete', selected.length, { count: selected.length }) }}
      <v-list dense>
        <v-list-item v-for="group in selected" :key="group.id">
          <v-list-item-content>
            <v-list-item-title>{{ group.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="grey darken-1" text @click="$emit('cancel')">
        {{ $t('generic.cancel') }}
      </v-btn>
      <v-btn color="error" text @click="$emit('remove')">
        {{ $t('generic.delete') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import type { PropType } from 'vue'
import { Group } from '@/domain/models/group/group'

export default Vue.extend({
  props: {
    selected: {
      type: Array as PropType<Group[]>,
      required: true
    }
  }
})
</script>
