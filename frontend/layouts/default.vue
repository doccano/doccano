<template>
  <v-app>
    <the-header />
    <nuxt />
    <the-footer />
  </v-app>
</template>

<script>
import TheFooter from '@/components/organisms/layout/TheFooter'
import TheHeader from '@/components/organisms/layout/TheHeader'

export default {
  components: {
    TheFooter,
    TheHeader
  }
}
</script>
