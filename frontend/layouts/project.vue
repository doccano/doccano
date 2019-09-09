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
        <side-bar-left />
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
import SideBarLeft from '~/components/project/SideBarLeft'

export default {
  components: {
    BaseLayout,
    SideBarLeft
  },
  data: () => ({
    drawerLeft: false
  })
}
</script>
