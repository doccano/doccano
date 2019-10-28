<template>
  <section>
    <v-parallax
      src="/images/vbanner.jpg"
      height="400"
      dark
    >
      <v-container>
        <v-layout
          wrap
          align-center
          justify-center
          class="white--text"
        >
          <v-flex
            xs12
            md7
          >
            <v-img
              src="http://doccano.herokuapp.com/static/images/named_entity_recognition.6fb82064e7aa.png"
              max-height="380"
              contain
              class="ma-5"
            />
          </v-flex>
          <v-flex
            xs12
            md5
          >
            <h1 class="mb-2 display-1 text-xs-center">
              Realize your ideas quickly
            </h1>
            <div class="mt-4">
              <v-menu open-on-hover offset-y>
                <template v-slot:activator="{ on }">
                  <v-btn
                    class="blue lighten-2"
                    dark
                    large
                    v-on="on"
                  >
                    Try demo
                    <v-icon>mdi-menu-down</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item
                    v-for="(item, index) in items"
                    :key="index"
                    @click="$router.push('/demo/' + item.link)"
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

<script>
export default {
  data() {
    return {
      items: [
        { title: 'Named Entity Recognition', link: 'named-entity-recognition' },
        { title: 'Sentiment Analysis', link: 'sentiment-analysis' },
        { title: 'Translation', link: 'translation' },
        { title: 'Text to SQL', link: 'text-to-sql' }
      ]
    }
  }
}
</script>
