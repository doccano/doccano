<template>
  <base-layout>
    <template #leftDrawerIcon>
      <v-app-bar-nav-icon @click="drawerLeft = !drawerLeft" />
    </template>

    <template #rightDrawerIcon>
      <v-app-bar-nav-icon @click="toggle" />
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
      <nuxt />
    </template>
  </base-layout>
</template>

<script>
import { mapMutations } from 'vuex'
import BaseLayout from '~/layouts/BaseLayout'
import SideBarLeft from '~/components/organisms/SideBarLeft'

export default {
  components: {
    BaseLayout,
    SideBarLeft
  },
  data: () => ({
    drawerLeft: false,
    drawerRight: false
  }),
  methods: {
    ...mapMutations({
      toggle: 'sidebar/toggle'
    })
  }
}
</script>
