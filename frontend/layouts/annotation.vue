<template>
  <v-app>
    <the-header>
      <template #leftDrawerIcon>
        <v-app-bar-nav-icon @click="drawerLeft = !drawerLeft" />
      </template>
    </the-header>

    <v-navigation-drawer
      v-model="drawerLeft"
      app
      clipped
      color=""
    >
      <the-side-bar />
    </v-navigation-drawer>

    <nuxt />
  </v-app>
</template>

<script>
import TheSideBar from '~/components/organisms/layout/TheSideBar'
import TheHeader from '~/components/organisms/layout/TheHeader'

export default {
  components: {
    TheSideBar,
    TheHeader
  },
  data() {
    return {
      drawerLeft: false
    }
  }
}
</script>
