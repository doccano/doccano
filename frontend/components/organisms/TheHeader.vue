<template>
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
</template>

<style scoped>
.top{
  text-decoration: none;
}
</style>
