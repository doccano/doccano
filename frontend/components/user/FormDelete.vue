<template>
  <v-card>
    <v-card-title class="headline">{{ $t('generic.delete') }}</v-card-title>
    <v-card-text>
      {{ $t('generic.deleteConfirm') }}
      <ul>
        <li v-for="item in selected" :key="item.id">
          {{ item.username }}
        </li>
      </ul>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="grey" text @click.stop="$emit('cancel')">{{ $t('generic.cancel') }}</v-btn>
      <v-btn color="error" text @click.stop="$emit('remove')">{{ $t('generic.delete') }}</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { PropType } from 'vue'
import { User } from '~/domain/models/user/user'

export default Vue.extend({
  props: {
    selected: {
      type: Array as PropType<User[]>,
      default: () => [],
      required: true
    }
  }
})
</script>
