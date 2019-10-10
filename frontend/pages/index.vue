<template>
  <v-content>
    <the-top-banner />
    <feature-cards />
    <the-bottom-banner />
  </v-content>
</template>

<script>
import FeatureCards from '@/components/organisms/FeatureCards'
import TheTopBanner from '@/components/organisms/TheTopBanner'
import TheBottomBanner from '@/components/organisms/TheBottomBanner'

export default {
  components: {
    FeatureCards,
    TheTopBanner,
    TheBottomBanner
  }
}
</script>
