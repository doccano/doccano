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
      <svg style="width:100px" x="0px" y="0px" viewBox="0 0 723.02 175.14"><g><path d="M42.27,38.82H0V0.24h130.94v38.58H88.62l0.02,113.06H42.3L42.27,38.82z M42.09,38.55"></path><path d="M169.5,102.33c-5.09,2.51-10.82,3.96-16.52,5.2c-9.33,2.07-14.21,4.36-14.24,11.76c-0.03,5.09,5.44,10.19,13.05,10.24c9.52,0.05,16.95-5.61,17.66-17.04L169.5,102.33z M209.56,127.33c-0.06,8.25,0.31,17.56,4.92,24.57l-42.73-0.25c-1.04-2.97-1.65-7.42-1.41-10.37h-0.43c-8.94,10.1-21.86,12.98-35.41,12.91c-21.15-0.13-38.65-10.38-38.52-33.44c0.21-34.7,40.83-33.19,62.21-37.08c5.72-1.03,11.44-2.69,11.47-9.67c0.05-7.41-6.91-10.21-13.68-10.24c-12.9-0.06-15.49,6.47-15.72,11.12l-38.93-0.22c1.44-30.88,30.66-35.79,56.69-35.64c52.46,0.31,51.92,22.1,51.78,43.25L209.56,127.33z M209.56,127.33"></path><path d="M274.13,70.16c-15.02-0.09-18.48,14.07-18.56,26.96c-0.08,13.11,3.23,27.32,18.24,27.41c15.03,0.08,18.49-14.07,18.57-27.2C292.46,84.44,289.15,70.23,274.13,70.16 M215.73,0h41.88l-0.3,54.41h0.42c6.4-9.27,17.64-14.71,30.13-14.64c36.8,0.22,46.56,31.58,46.41,57.4c-0.16,27.5-15.36,58.08-46.45,57.91c-20.52-0.13-26.82-7.99-32.07-15.01h-0.42l-0.08,11.81h-39.52V0z M215.73,0.85"></path><path d="M393.05,30.73c-15.87-0.1-18.08,15.34-18.15,26.97c-0.06,11.63,1.96,27.31,17.82,27.4c15.86,0.09,18.08-15.55,18.15-27.2C410.94,46.27,408.91,30.82,393.05,30.73 M392.55,115.56c-41.26-0.24-59.72-27.64-59.53-58.1c0.18-30.47,18.94-57.43,60.2-57.18c41.26,0.23,59.72,27.41,59.54,57.88C452.57,88.61,433.81,115.8,392.55,115.56"></path><path d="M497,30.72c-15.86-0.1-18.07,15.34-18.13,26.98c-0.08,11.63,1.95,27.3,17.82,27.39c15.85,0.1,18.07-15.55,18.14-27.19C514.89,46.27,512.86,30.81,497,30.72 M496.5,115.56c-41.25-0.25-59.71-27.65-59.52-58.11c0.17-30.46,18.94-57.43,60.19-57.19c41.25,0.24,59.71,27.42,59.54,57.88C556.53,88.62,537.76,115.79,496.5,115.56"></path><path d="M561.23,0.27h41l0,151.61h-41V0.27z M561.23,0.27"></path><path d="M678.57,101.97c-5.09,2.5-10.82,3.95-16.52,5.18c-9.34,2.07-14.2,4.37-14.25,11.77c-0.03,5.08,5.44,10.18,13.05,10.23c9.53,0.05,16.96-5.61,17.66-17.04L678.57,101.97z M718.89,126.94c-0.04,8.25-0.5,17.93,4.12,24.94h-42.1c-1.03-2.97-1.74-8.03-1.5-10.98l-0.43-0.01c-8.94,10.1-21.85,12.99-35.4,12.91c-21.16-0.14-38.66-10.39-38.52-33.45c0.21-34.7,40.81-33.18,62.2-37.07c5.72-1.03,11.44-2.69,11.48-9.67c0.05-7.41-6.91-10.2-13.69-10.24c-12.91-0.07-15.48,6.47-15.71,11.12l-38.95-0.21c1.45-30.88,30.68-35.8,56.7-35.63c52.46,0.29,51.92,22.09,51.79,43.24V126.94z M718.89,126.94"></path><path d="M348.73,115.57c29.74,13.29,60.6,19.19,94.23,19.38c35.33,0.21,62.12-6.46,96.03-19.38l-0.2,36.6c-30.35,15.05-63.27,23.17-96.07,22.98c-35.75-0.21-61.51-7.55-94.21-22.98L348.73,115.57z M348.73,115.57"></path></g></svg>
    </nuxt-link>
    
    <v-toolbar-title
      v-if="!isAuthenticated"
      class="ml-2 d-none d-sm-flex"
    >
     Doccano
    </v-toolbar-title>
    <v-btn
      v-if="isAuthenticated && isIndividualProject"
      text
      class="d-none d-sm-flex"
      style="text-transform:none"
    >
      <v-icon small class="mr-1">
        mdi-hexagon-multiple
      </v-icon>
      <span> {{ currentProject.name }}</span>
    </v-btn>
    <div class="flex-grow-1" />
    <the-color-mode-switcher />
    <locale-menu />
    <v-btn
      v-if="isAuthenticated"
      text
      class="text-capitalize"
      @click="$router.push(localePath('/projects'))"
    >
      {{ $t('header.projects') }}
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
          {{ $t('home.demoDropDown') }}
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
      @click="$router.push(localePath('/auth'))"
    >
      {{ $t('user.login') }}
    </v-btn>
    <v-menu
      v-if="isAuthenticated"
      offset-y
    >
      <template v-slot:activator="{ on }">
        <v-btn on icon v-on="on">
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-subheader>{{ getUsername }}</v-subheader>
        <v-list-item @click="signout">
          <v-list-item-icon>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              {{ $t('user.signOut') }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import TheColorModeSwitcher from './TheColorModeSwitcher'
import LocaleMenu from './LocaleMenu'

export default {
  components: {
    TheColorModeSwitcher,
    LocaleMenu
  },

  data() {
    return {
      items: [
        { title: this.$t('home.demoNER'), link: 'named-entity-recognition' },
        { title: this.$t('home.demoSent'), link: 'sentiment-analysis' },
        { title: this.$t('home.demoTranslation'), link: 'translation' },
        { title: this.$t('home.demoTextToSQL'), link: 'text-to-sql' }
      ]
    }
  },

  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'getUsername']),
    ...mapGetters('projects', ['currentProject']),

    isIndividualProject() {
      return this.$route.name && this.$route.name.startsWith('projects-id')
    }
  },

  methods: {
    ...mapActions('auth', ['logout']),
    signout() {
      this.logout()
      this.$router.push(this.localePath('/'))
    }
  }
}
</script>
