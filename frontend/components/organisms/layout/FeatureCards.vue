<template>
  <v-container>
    <v-layout
      column
      wrap
      class="my-5"
      align-center
    >
      <v-flex xs12 sm4 class="my-3">
        <div class="text-xs-center">
          <h2 class="headline">
            {{ $t('home.featuresTitle') }}
          </h2>
        </div>
      </v-flex>
      <v-flex xs12>
        <v-container grid-list-xl>
          <v-layout wrap align-center>
            <v-flex
              v-for="(item, index) in featureCards"
              :key="index"
              xs12
              md4
            >
              <feature-card
                :image-src="item.imageSrc"
                :title="item.title"
                :text="item.text"
              />
            </v-flex>
          </v-layout>
        </v-container>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import FeatureCard from '@/components/organisms/layout/FeatureCard'

export default {
  components: {
    FeatureCard
  },

  data() {
    return {
      featureCards: [
        {
          imageSrc: '/images/feature3.png',
          title: this.$t('home.featuresTitle1'),
          text: this.$t('home.featuresText1')
        },
        {
          imageSrc: '/images/feature2.png',
          title: this.$t('home.featuresTitle2'),
          text: this.$t('home.featuresText2')
        },
        {
          imageSrc: '/images/feature1.png',
          title: this.$t('home.featuresTitle3'),
          text: this.$t('home.featuresText3')
        }
      ]
    }
  }
}
</script>
