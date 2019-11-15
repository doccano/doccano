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
      <v-container fluid>
        <v-row
          no-gutters
          class="d-none d-sm-flex"
        >
          <v-col v-if="currentDoc">
            <approve-button :approved="approved" />
            <filter-button />
            <guideline-button />
          </v-col>
          <v-spacer />
          <v-col>
            <paginator />
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" md="9">
            <nuxt />
          </v-col>
          <v-col cols="12" md="3">
            <metadata-box
              v-if="currentDoc"
              :metadata="JSON.parse(currentDoc.meta)"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-content>

    <bottom-navigator class="d-flex d-sm-none" />
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import TheSideBar from '~/components/organisms/layout/TheSideBar'
import TheHeader from '~/components/organisms/layout/TheHeader'
import BottomNavigator from '@/components/containers/annotation/BottomNavigator'
import Paginator from '~/components/containers/annotation/Paginator'
import GuidelineButton from '@/components/containers/annotation/GuidelineButton'
import MetadataBox from '@/components/organisms/annotation/MetadataBox'
import FilterButton from '@/components/containers/annotation/FilterButton'
import ApproveButton from '@/components/containers/annotation/ApproveButton'

export default {
  middleware: ['check-auth', 'auth'],

  components: {
    TheSideBar,
    TheHeader,
    BottomNavigator,
    Paginator,
    GuidelineButton,
    FilterButton,
    ApproveButton,
    MetadataBox
  },
  data() {
    return {
      drawerLeft: false
    }
  },

  computed: {
    ...mapGetters('projects', ['getLink', 'getCurrentUserRole']),
    ...mapGetters('documents', ['currentDoc', 'approved'])
  },

  created() {
    this.setCurrentProject(this.$route.params.id)
  },

  methods: {
    ...mapActions('projects', ['setCurrentProject'])
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
