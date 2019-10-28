<template>
  <v-content>
    <the-top-banner />
    <feature-cards />
    <the-bottom-banner />
  </v-content>
</template>

<script>
import FeatureCards from '@/components/organisms/home/FeatureCards'
import TheTopBanner from '@/components/organisms/home/TheTopBanner'
import TheBottomBanner from '@/components/organisms/home/TheBottomBanner'

export default {
  components: {
    FeatureCards,
    TheTopBanner,
    TheBottomBanner
  }
}
</script>
