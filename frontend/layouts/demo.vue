<template>
  <v-app>
    <the-header />
    <nuxt />
  </v-app>
</template>

<script>
import TheHeader from '~/components/organisms/TheHeader'

export default {
  components: {
    TheHeader
  }
}
</script>
