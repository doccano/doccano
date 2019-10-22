<template>
  <v-app-bar
    app
    clipped-left
  >
    <slot name="leftDrawerIcon" />
    <nuxt-link to="/" style="line-height:0;">
      <img src="~/assets/icon.png" height="48">
    </nuxt-link>
    <v-toolbar-title class="ml-2 d-none d-sm-flex">
      doccano
    </v-toolbar-title>
    <div class="flex-grow-1" />
    <v-menu open-on-hover offset-y>
      <template v-slot:activator="{ on }">
        <v-btn
          text
          v-on="on"
        >
          Demo
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
    <v-btn
      outlined
      @click="$router.push('/auth')"
    >
      Sign in
    </v-btn>
    <the-top-menu />
  </v-app-bar>
</template>

<script>
import TheTopMenu from '@/components/organisms/TheTopMenu'

export default {
  components: {
    TheTopMenu
  },

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

<style scoped>
.top{
  text-decoration: none;
}
</style>
