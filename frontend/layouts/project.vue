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
      <the-side-bar
        :link="getLink"
        :role="getCurrentUserRole"
      />
    </v-navigation-drawer>

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
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
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
  },

  computed: {
    ...mapGetters('projects', ['getLink', 'getCurrentUserRole'])
  },

  created() {
    this.setCurrentProject(this.$route.params.id)
  },

  methods: {
    ...mapActions('projects', ['setCurrentProject'])
  }
}
</script>
