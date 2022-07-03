<template>
  <v-card>
    <v-list dense>
      <v-list-item-group v-model="model">
        <v-list-item
          v-for="(item, i) in regions"
          :key="`item-${i}`"
          :value="item"
          active-class="text--accent-4"
          @mouseenter="$emit('hover-region', item.id)"
          @mouseleave="$emit('unhover-region', item.id)"
        >
          <template #default="{}">
            <v-list-item-content>
              <v-list-item-title>
                <v-chip :color="item.color" text-color="white" small v-text="item.category" />
              </v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-checkbox
                :input-value="item.visibility"
                :on-icon="mdiEyeOutline"
                :off-icon="mdiEyeOffOutline"
                @change="$emit('change-visibility', item.id, $event)"
              />
            </v-list-item-action>
          </template>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
import { mdiEyeOutline, mdiEyeOffOutline } from '@mdi/js'

export default {
  props: {
    regions: {
      type: Array,
      default: () => []
    }
  },

  data() {
    return {
      mdiEyeOutline,
      mdiEyeOffOutline,
      model: null,
      headers: [
        {
          text: 'Category',
          align: 'start',
          value: 'category'
        },
        { text: 'Visibility', value: 'visibility' }
      ]
    }
  }
}
</script>
