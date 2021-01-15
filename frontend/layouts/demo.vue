<template>
  <v-app>
    <the-header />
    <nuxt />
  </v-app>
</template>

<script>
import TheHeader from '~/components/organisms/layout/TheHeader'

export default {
  middleware: ['check-auth'],
  components: {
    TheHeader
  }
}
</script>
