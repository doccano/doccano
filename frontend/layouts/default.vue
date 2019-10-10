<template>
  <v-app>
    <the-header />
    <nuxt />
    <the-footer />
  </v-app>
</template>

<script>
import TheFooter from '@/components/organisms/TheFooter'
import TheHeader from '@/components/organisms/TheHeader'

export default {
  components: {
    TheFooter,
    TheHeader
  }
}
</script>
