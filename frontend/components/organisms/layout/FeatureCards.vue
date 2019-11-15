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
            The best features
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
          title: 'Team Collaboration',
          text: 'Annotation with your team mates'
        },
        {
          imageSrc: '/images/feature2.png',
          title: 'Any Language',
          text: 'Annotation with any language'
        },
        {
          imageSrc: '/images/feature1.png',
          title: 'Open Source',
          text: 'Annotation with free and customizable'
        }
      ]
    }
  }
}
</script>
