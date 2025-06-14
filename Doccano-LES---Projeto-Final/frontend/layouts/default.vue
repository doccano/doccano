<template>
  <v-app>
    <the-header />
    <nuxt />
    <the-footer />
  </v-app>
</template>

<script>
import TheFooter from '@/components/layout/TheFooter'
import TheHeader from '@/components/layout/TheHeader'

export default {
  components: {
    TheFooter,
    TheHeader
  }
}
</script>
