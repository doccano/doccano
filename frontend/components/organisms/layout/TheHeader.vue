<template>
  <v-app-bar
    app
    clipped-left
  >
    <slot name="leftDrawerIcon" />
    <nuxt-link
      v-if="!isAuthenticated"
      to="/"
      style="line-height:0;"
    >
      <img src="~/assets/icon.png" height="48">
    </nuxt-link>
    <v-toolbar-title
      v-if="!isAuthenticated"
      class="ml-2 d-none d-sm-flex"
    >
      doccano
    </v-toolbar-title>
    <div class="flex-grow-1" />
    <the-color-mode-switcher />
    <v-btn
      v-if="isAuthenticated"
      text
      @click="$router.push('/projects')"
    >
      Projects
    </v-btn>
    <v-menu
      v-if="!isAuthenticated"
      open-on-hover
      offset-y
    >
      <template v-slot:activator="{ on }">
        <v-btn
          text
          v-on="on"
        >
          Demo
          <v-icon>mdi-menu-down</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          @click="$router.push('/demo/' + item.link)"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-btn
      v-if="!isAuthenticated"
      outlined
      @click="$router.push('/auth')"
    >
      Sign in
    </v-btn>
    <v-menu
      v-if="isAuthenticated"
      bottom
    >
      <template v-slot:activator="{ on }">
        <v-btn
          icon
          v-on="on"
        >
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item @click="signout">
          <v-list-item-icon>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              Sign out
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import TheColorModeSwitcher from '@/components/organisms/layout/TheColorModeSwitcher'

export default {
  components: {
    TheColorModeSwitcher
  },

  data() {
    return {
      items: [
        { title: 'Named Entity Recognition', link: 'named-entity-recognition' },
        { title: 'Sentiment Analysis', link: 'sentiment-analysis' },
        { title: 'Translation', link: 'translation' },
        { title: 'Text to SQL', link: 'text-to-sql' }
      ]
    }
  },

  computed: {
    ...mapGetters('auth', ['isAuthenticated'])
  },

  methods: {
    ...mapActions('auth', ['logout']),
    signout() {
      this.logout()
      this.$router.push('/')
    }
  }
}
</script>
