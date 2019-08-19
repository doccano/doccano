<template>
  <v-app>
    <v-app-bar
      color="indigo lighten-1"
      dark
      app
    >
      <v-toolbar-title v-text="title" />
    </v-app-bar>
    <nuxt />
    <v-footer
      color="primary lighten-1"
      padless
    >
      <v-layout
        justify-center
        wrap
      >
        <v-flex
          primary
          lighten-2
          py-4
          text-center
          white--text
          xs12
        >
          {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
        </v-flex>
      </v-layout>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      title: 'doccano',
      links: [
        'Home',
        'About Us',
        'Team',
        'Services',
        'Blog',
        'Contact Us'
      ]
    }
  }
}
</script>
