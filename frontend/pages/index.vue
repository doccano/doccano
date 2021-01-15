<template>
  <v-content>
    <the-top-banner />
    <feature-cards />
    <the-bottom-banner />
  </v-content>
</template>

<script>
import FeatureCards from '@/components/organisms/layout/FeatureCards'
import TheTopBanner from '@/components/organisms/layout/TheTopBanner'
import TheBottomBanner from '@/components/organisms/layout/TheBottomBanner'

export default {
  components: {
    FeatureCards,
    TheTopBanner,
    TheBottomBanner
  }
}
</script>
