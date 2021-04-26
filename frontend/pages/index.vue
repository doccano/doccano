<template>
  <v-main style="background: black;">
    <the-top-banner />
    <feature-cards />
    <the-bottom-banner />
  </v-main>
</template>

<script>
import TheTopBanner from '@/components/layout/TheTopBanner'

export default {
  components: {
    TheTopBanner,
  }
}
</script>
