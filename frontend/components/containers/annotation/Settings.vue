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
          <h3>Auto Labeling</h3>
          <p>
            The auto labeling allows users to annotate data automatically.
            It enables them to speed up annotating data.
            You only have to correct labels which are mislabeled by the system and annotate labels which aren’t labeled by it.
          </p>
          <p>
            Notice that you can't use this feature unless the project administrators configure the auto labeling.
            Also, depending on the configuration, it will take some cost for the administrators(e.g. In the case of configuring some paid service like AWS or GCP).
          </p>
          <v-switch
            v-model="value.onAutoLabeling"
          />
          <v-alert
            v-if="errors.autoLabelingConfig"
            prominent
            type="error"
          >
            <v-row align="center">
              <v-col class="grow">
                {{ errors.autoLabelingConfig }}
              </v-col>
            </v-row>
          </v-alert>
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

  props: {
    value: {
      type: Object,
      default: () => {},
      required: true
    },
    errors: {
      type: Object,
      default: () => {},
      required: true
    }
  },

  data() {
    return {
      dialog: false
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
