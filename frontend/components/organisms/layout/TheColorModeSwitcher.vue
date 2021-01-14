<template>
  <v-btn
    icon
    fab
    @click="isDark=!isDark"
  >
    <v-icon v-if="isDark">
      mdi-moon-waxing-crescent
    </v-icon>
    <v-icon v-else>
      mdi-white-balance-sunny
    </v-icon>
  </v-btn>
</template>

<script>
export default {
  data() {
    return {
      isDark: false
    }
  },

  watch: {
    isDark() {
      this.$vuetify.theme.dark = this.isDark
      localStorage.setItem('dark', this.isDark)
    }
  },

  created() {
    const dark = localStorage.getItem('dark')
    this.isDark = dark ? JSON.parse(dark) : false
  }
}
</script>
