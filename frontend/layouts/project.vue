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
        :is-project-admin="isProjectAdmin"
        :project="currentProject"
      />
    </v-navigation-drawer>

    <v-main>
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
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import TheSideBar from '~/components/layout/TheSideBar'
import TheHeader from '~/components/layout/TheHeader'

export default {

  components: {
    TheSideBar,
    TheHeader
  },
  middleware: ['check-auth', 'auth', 'check-admin'],

  data() {
    return {
      drawerLeft: null,
      isProjectAdmin: false,
    }
  },

  computed: {
    ...mapGetters('projects', ['getLink', 'currentProject']),
  },

  async created() {
    this.isProjectAdmin = await this.$services.member.isProjectAdmin(this.$route.params.id)
  }
}
</script>
