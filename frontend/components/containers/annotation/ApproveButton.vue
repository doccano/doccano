<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        class="text-capitalize ps-1 pe-1"
        min-width="36"
        outlined
        v-on="on"
        @click="approveDocument"
      >
        <v-icon v-if="approved">
          mdi-check-circle-outline
        </v-icon>
        <v-icon v-else>
          mdi-checkbox-blank-circle-outline
        </v-icon>
      </v-btn>
    </template>
    <span>Approve</span>
  </v-tooltip>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  props: {
    approved: {
      type: Boolean,
      default: false,
      required: true
    }
  },

  methods: {
    ...mapActions('documents', ['approve']),
    approveDocument() {
      this.approve({
        projectId: this.$route.params.id
      })
    }
  }
}
</script>
