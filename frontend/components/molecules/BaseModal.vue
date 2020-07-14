<template>
  <v-dialog
    v-model="dialog"
    width="800px"
  >
    <template v-slot:activator="{}">
      <v-btn
        :class="classObject"
        :color="color"
        :outlined="isOutlined"
        :disabled="disabled"
        class="mb-2 text-capitalize"
        @click="dialog=true"
      >
        {{ text }}
      </v-btn>
    </template>
    <slot :close="close" />
  </v-dialog>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: '',
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    },
    isCreate: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      dialog: false
    }
  },

  computed: {
    classObject() {
      return this.isCreate ? [] : ['ml-2']
    },
    color() {
      return this.isCreate ? 'primary' : ''
    },
    isOutlined() {
      return !this.isCreate
    }
  },

  methods: {
    close() {
      this.dialog = false
    }
  }
}
</script>
