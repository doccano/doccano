<template>
  <v-app>
    <the-header />
    <nuxt />
  </v-app>
</template>

<script>
import TheHeader from '~/components/layout/TheHeader'

export default {
  components: {
    TheHeader
  }
}
</script>
