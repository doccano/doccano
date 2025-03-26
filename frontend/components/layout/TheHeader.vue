<template>
  <v-app-bar app clipped-left>
    <slot name="leftDrawerIcon" />
    <nuxt-link v-if="!isAuthenticated" to="/" style="line-height: 0">
      <img src="~/assets/icon.png" height="48" />
    </nuxt-link>
    <v-toolbar-title v-if="!isAuthenticated" class="ml-2 d-none d-sm-flex">
      doccano
    </v-toolbar-title>
    <v-btn
      v-if="isAuthenticated && isIndividualProject"
      text
      class="d-none d-sm-flex"
      style="text-transform: none"
    >
      <v-icon small class="mr-1">
        {{ mdiHexagonMultiple }}
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
    <v-btn
      v-if="isAuthenticated && isStaff"
      text
      class="text-capitalize"
      @click="$router.push(localePath('/users'))"
    >
      {{ $t('header.users') }}
    </v-btn>
    <v-menu v-if="!isAuthenticated" open-on-hover offset-y>
      <template #activator="{ on }">
        <v-btn text v-on="on">
          {{ $t('home.demoDropDown') }}
          <v-icon>{{ mdiMenuDown }}</v-icon>
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
    <v-btn v-if="!isAuthenticated" outlined class="mr-2" @click="$router.push(localePath('/auth'))">
      {{ $t('user.login') }}
    </v-btn>
    <v-btn v-if="isStaff" outlined color="success" 
    @click="$router.push(localePath('/register'))">
      {{ $t('user.register') }}
    </v-btn>
    <v-menu v-if="isAuthenticated" offset-y z-index="200">
      <template #activator="{ on }">
        <v-btn on icon v-on="on">
          <v-icon>{{ mdiDotsVertical }}</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-subheader>{{ getUsername }}</v-subheader>
        <v-list-item>
          <v-list-item-content>
            <v-switch :input-value="isRTL" :label="direction" class="ms-1" @change="toggleRTL" />
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="signout">
          <v-list-item-icon>
            <v-icon>{{ mdiLogout }}</v-icon>
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
import { mdiLogout, mdiDotsVertical, mdiMenuDown, mdiHexagonMultiple } from '@mdi/js'
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
        {
          title: this.$t('home.demoIntenDetectSlotFil'),
          link: 'intent-detection-and-slot-filling'
        },
        { title: this.$t('home.demoTextToSQL'), link: 'text-to-sql' },
        { title: this.$t('home.demoImageClas'), link: 'image-classification' },
        { title: this.$t('home.demoImageCapt'), link: 'image-caption' },
        { title: this.$t('home.demoObjDetect'), link: 'object-detection' },
        { title: this.$t('home.demoPolygSegm'), link: 'segmentation' },
        { title: this.$t('home.demoSTT'), link: 'speech-to-text' }
      ],
      mdiLogout,
      mdiDotsVertical,
      mdiMenuDown,
      mdiHexagonMultiple
    }
  },

  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'isStaff', 'getUsername']),
    ...mapGetters('projects', ['currentProject']),
    ...mapGetters('config', ['isRTL']),

    isIndividualProject() {
      return this.$route.name && this.$route.name.startsWith('projects-id')
    },

    direction() {
      return this.isRTL ? 'RTL' : 'LTR'
    }
  },

  methods: {
    ...mapActions('auth', ['logout']),
    ...mapActions('config', ['toggleRTL']),
    signout() {
      this.logout()
      this.$router.push(this.localePath('/'))
    }
  }
}
</script>
