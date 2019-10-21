<template>
  <v-app id="keep">
    <v-app-bar
      app
      clipped-left
      clipped-right
      color=""
    >
      <slot name="leftDrawerIcon" />
      <nuxt-link to="/" class="top">
        <span class="title ml-3 mr-5">doccano</span>
      </nuxt-link>
      <v-spacer />
      <slot name="rightDrawerIcon" />
    </v-app-bar>

    <slot name="leftDrawer" />
    <slot name="rightDrawer" />

    <slot name="content" />
  </v-app>
</template>

<style scoped>
.top{
  text-decoration: none;
}
</style>
