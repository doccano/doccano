<template>
  <v-dialog v-model="internalDialog" max-width="400px">
    <v-card>
      <v-card-title class="headline">
        Confirm Delete
      </v-card-title>
      <v-alert v-if="dbError" type="error" dense>
        {{ dbError }}
      </v-alert>
      <v-card-text>
        {{ deleteDialogText }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="red" text @click="confirmDelete" :disabled="isDeleting || !!dbError">
          Delete
        </v-btn>
        <v-btn color="grey" text @click="cancelDelete">
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
// @ts-nocheck
import Vue from 'vue'
export default Vue.extend({
  name: 'DeleteDialog',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    dbError: {
      type: String,
      default: ''
    },
    deleteDialogText: {
      type: String,
      default: ''
    },
    isDeleting: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    internalDialog: {
      get() {
        return this.value
      },
      set(val: boolean) {
        this.$emit('input', val)
      }
    }
  },
  methods: {
    confirmDelete() {
      this.$emit('confirm-delete')
    },
    cancelDelete() {
      this.$emit('cancel-delete')
    }
  }
})
</script>

<style scoped>
</style>