<template>
  <v-app>
    <v-app-bar
      app
      color=""
    >
      <nuxt-link to="/" style="line-height:0;">
        <img src="~/assets/icon.png" height="48">
      </nuxt-link>
      <v-toolbar-title class="align-center ml-2">
        doccano
      </v-toolbar-title>
      <div class="flex-grow-1" />
      <v-btn
        outlined
        href="auth"
      >
        Sign in
      </v-btn>
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
          black
          lighten-2
          py-4
          text-center
          white--text
          xs12
        >
          &copy; {{ new Date().getFullYear() }} doccano
        </v-flex>
      </v-layout>
    </v-footer>
  </v-app>
</template>

<script>
export default {}
</script>

<style scoped>
.top{
  text-decoration: none;
}
</style>
