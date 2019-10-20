<template>
  <base-layout>
    <template #leftDrawerIcon>
      <v-app-bar-nav-icon @click="drawerLeft = !drawerLeft" />
    </template>

    <template #leftDrawer>
      <v-navigation-drawer
        v-model="drawerLeft"
        app
        clipped
        color=""
      >
        <the-side-bar />
      </v-navigation-drawer>
    </template>

    <template #content>
      <v-content>
        <v-container
          fluid
          fill-height
        >
          <v-layout
            justify-center
          >
            <v-flex fill-height>
              <nuxt />
            </v-flex>
          </v-layout>
        </v-container>
      </v-content>
    </template>
  </base-layout>
</template>

<script>
import BaseLayout from '~/layouts/BaseLayout'
import TheSideBar from '~/components/organisms/TheSideBar'

export default {
  components: {
    BaseLayout,
    TheSideBar
  },
  data: () => ({
    drawerLeft: false
  })
}
</script>
