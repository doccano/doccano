<template>
  <v-btn-toggle
    v-model="option"
    mandatory
  >
    <v-btn icon>
      <v-icon>mdi-format-list-bulleted</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>mdi-text</v-icon>
    </v-btn>
  </v-btn-toggle>
</template>

<script>
export default {
  data() {
    return {
      option: 0
    }
  },

  watch: {
    option(val) {
      if (val === 0) {
        this.$emit('change', 'label-group')
      } else {
        this.$emit('change', 'label-select')
      }
    }
  }
}
</script>
