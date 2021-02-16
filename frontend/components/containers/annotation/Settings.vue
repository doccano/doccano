<template>
  <div style="display:inline;">
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          class="text-capitalize ps-1 pe-1"
          min-width="36"
          icon
          v-on="on"
          @click="dialog=true"
        >
          <v-icon>
            mdi-cog-outline
          </v-icon>
        </v-btn>
      </template>
      <span>Settings</span>
    </v-tooltip>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <base-card
        title="Settings"
        :cancel-text="$t('generic.close')"
        @cancel="dialog=false"
      >
        <template #content>
          <v-switch
            v-model="value.onAutoLabeling"
            label="Auto Labeling"
          />
        </template>
      </base-card>
    </v-dialog>
  </div>
</template>

<script>
import BaseCard from '@/components/molecules/BaseCard'

export default {
  components: {
    BaseCard
  },

  data() {
    return {
      dialog: false
    }
  },

  props: {
    value: {
      type: Object,
      default: () => {},
      required: true
    }
  },

  watch: {
    value: {
      handler(val) {
        this.$emit('input', val)
      },
      deep: true
    }
  }
}
</script>
