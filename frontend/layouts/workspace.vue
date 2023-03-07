<template>
  <v-app>
    <the-header>
      <template #leftDrawerIcon>
        <v-app-bar-nav-icon @click="drawerLeft = !drawerLeft" />
      </template>
    </the-header>

    <v-navigation-drawer v-model="drawerLeft" app clipped>
      <the-side-bar :is-project-admin="isProjectAdmin" :project="currentProject" />
    </v-navigation-drawer>

    <v-main class="pb-0">
      <nuxt />
    </v-main>
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
  middleware: ['check-auth', 'auth', 'set-project'],

  data() {
    return {
      drawerLeft: null,
      isProjectAdmin: false
    }
  },

  computed: {
    ...mapGetters('projects', ['currentProject'])
  },

  watch: {
    '$route.query'() {
      this.$services.option.save(this.$route.params.id, this.$route.query)
    }
  },

  async created() {
    const member = await this.$repositories.member.fetchMyRole(this.$route.params.id)
    this.isProjectAdmin = member.isProjectAdmin
  }
}
</script>
