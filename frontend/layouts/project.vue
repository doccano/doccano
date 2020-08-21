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
import { mapActions, mapGetters } from 'vuex'
import TheSideBar from '~/components/organisms/layout/TheSideBar'
import TheHeader from '~/components/organisms/layout/TheHeader'

export default {
  middleware: ['check-auth', 'auth', 'check-admin'],

  components: {
    TheSideBar,
    TheHeader
  },

  data() {
    return {
      drawerLeft: null
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

<style>
/* dark mode styles */
.theme--dark .tui-editor-contents h1 {
  color: #fff; /* inversion of #000 */
}
.theme--dark .tui-editor-contents h2,
.theme--dark .tui-editor-contents h3,
.theme--dark .tui-editor-contents h4,
.theme--dark .tui-editor-contents h5,
.theme--dark .tui-editor-contents h6,
.theme--dark .tui-editor-contents code span {
  color: #ccc; /* inversion of #333 */
}
.theme--dark .tui-editor-contents blockquote {
  color: #888; /* inversion of #777777 */
}
.theme--dark .tui-editor-contents ul,
.theme--dark .tui-editor-contents menu,
.theme--dark .tui-editor-contents ol,
.theme--dark .tui-editor-contents dir,
.theme--dark .tui-editor-contents p,
.theme--dark .tui-editor-contents table {
  color: #aaa; /* inversion of #555555 */
}
.theme--dark .tui-editor-contents table td {
border: #151515; /* inversion of #eaeaea */
}
.theme--dark .tui-editor-contents table th {
  border: #8d8884; /* inversion of #72777b */
  background-color: #847e7b; /* inversion of #7b8184 */
}
.theme--dark .tui-editor-contents pre {
  background-color: #0a0807; /* inversion of #f5f7f8 */
}
.theme--dark .tui-editor-contents code {
  color: #3e8774; /* inversion of #c1788b */
}
</style>
