<template>
  <section>
    <v-parallax :src="require(`~/assets/vbanner.jpg`)" height="400" dark>
      <v-container>
        <v-layout wrap align-center justify-center class="white--text">
          <v-flex xs12 md7>
            <v-img :src="require(`~/assets/ner_demo.png`)" max-height="380" contain class="ma-5" />
          </v-flex>
          <v-flex xs12 md5>
            <h1 class="mb-2 display-1 text-xs-center">
              {{ $t('home.footerTitle') }}
            </h1>
            <div class="mt-4">
              <v-menu open-on-hover offset-y>
                <template #activator="{ on }">
                  <v-btn class="blue lighten-2" dark large v-on="on">
                    {{ $t('home.demoDropDown') }}
                    <v-icon>{{ mdiMenuDown }}</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item
                    v-for="(item, index) in items"
                    :key="index"
                    @click="$router.push(localePath('/demo/' + item.link))"
                  >
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-parallax>
  </section>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMenuDown } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      items: [
        { title: this.$t('home.demoNER'), link: 'named-entity-recognition' },
        { title: this.$t('home.demoSent'), link: 'sentiment-analysis' },
        { title: this.$t('home.demoTranslation'), link: 'translation' },
        { title: this.$t('home.demoTextToSQL'), link: 'text-to-sql' }
      ],
      mdiMenuDown
    }
  }
})
</script>
