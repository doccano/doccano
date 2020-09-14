<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        v-shortkey.once="['enter']"
        :disabled="disabled"
        class="text-capitalize ps-1 pe-1"
        min-width="36"
        outlined
        v-on="on"
        @shortkey="approveNextPage"
        @click="approveDocument"
      >
        <v-icon v-if="approved">
          mdi-check
        </v-icon>
        <v-icon v-else>
          mdi-close
        </v-icon>
      </v-btn>
    </template>
    <span v-if="approved">Checked</span>
    <span v-else>Not checked</span>
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
    },
    disabled: {
      type: Boolean,
      default: false
    },
    value: {
      type: Number,
      default: 1,
      required: true
    },
    length: {
      type: Number,
      default: 1,
      required: true
    }
  },

  methods: {
    ...mapActions('documents', ['approve']),
    approveDocument() {
      this.approve({
        projectId: this.$route.params.id
      })
    },
    /** Approves document and moves to the next page */
    approveNextPage() {
      const page = Math.min(this.value + 1, this.length)
      this.$emit('input', page)
      this.approveDocument()
    }
  }
}
</script>
