<template>
  <v-main>
    <the-top-banner />
    <feature-cards />
    <the-bottom-banner />
  </v-main>
</template>

<script>
import FeatureCards from '@/components/layout/FeatureCards'
import TheTopBanner from '@/components/layout/TheTopBanner'
import TheBottomBanner from '@/components/layout/TheBottomBanner'

export default {
  components: {
    FeatureCards,
    TheTopBanner,
    TheBottomBanner
  }
}
</script>
