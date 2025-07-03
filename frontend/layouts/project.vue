<template>
  <v-app>
    <the-header>
      <template #leftDrawerIcon>
        <v-app-bar-nav-icon @click="drawerLeft = !drawerLeft" />
      </template>
    </the-header>

    <v-navigation-drawer v-model="drawerLeft" app clipped color="">
      <the-side-bar :is-project-admin="isProjectAdmin" :project="currentProject" />
    </v-navigation-drawer>

    <v-main>
      <v-container fluid fill-height>
        <v-layout justify-center>
          <v-flex fill-height>
            <nuxt />
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>

    <!-- Global Notification Snackbar -->
    <v-snackbar
      v-model="showNotification"
      :color="notificationColor"
      :timeout="notificationTimeout"
      bottom
      right
    >
      {{ notificationText }}
      <template #action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="hideNotification"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import TheHeader from '~/components/layout/TheHeader'
import TheSideBar from '~/components/layout/TheSideBar'

export default {
  components: {
    TheSideBar,
    TheHeader
  },

  data() {
    return {
      drawerLeft: null,
      isProjectAdmin: false
    }
  },

  computed: {
    ...mapGetters('projects', ['currentProject']),
    ...mapGetters('notification', {
      showNotification: 'show',
      notificationText: 'text',
      notificationColor: 'color',
      notificationTimeout: 'timeout'
    })
  },

  async created() {
    const member = await this.$repositories.member.fetchMyRole(this.$route.params.id)
    this.isProjectAdmin = member.isProjectAdmin
  },

  methods: {
    hideNotification() {
      this.$store.dispatch('notification/hideNotification')
    }
  }
}
</script>
