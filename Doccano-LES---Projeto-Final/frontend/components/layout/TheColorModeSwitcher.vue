<template>
  <v-btn icon fab @click="isDark = !isDark">
    <v-icon v-if="isDark">
      {{ mdiMoonWaxingCrescent }}
    </v-icon>
    <v-icon v-else>
      {{ mdiWhiteBalanceSunny }}
    </v-icon>
  </v-btn>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMoonWaxingCrescent, mdiWhiteBalanceSunny } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      isDark: false,
      mdiMoonWaxingCrescent,
      mdiWhiteBalanceSunny
    }
  },

  watch: {
    isDark() {
      this.$vuetify.theme.dark = this.isDark
      localStorage.setItem('dark', JSON.stringify(this.isDark))
    }
  },

  created() {
    const dark = localStorage.getItem('dark')
    this.isDark = dark ? JSON.parse(dark) : false
  }
})
</script>
