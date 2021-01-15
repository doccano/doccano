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
      <v-overlay :value="loading">
        <v-progress-circular indeterminate size="64" />
      </v-overlay>
      <v-container fluid>
        <v-row
          no-gutters
          class="d-none d-sm-flex"
        >
          <v-col>
            <approve-button
              v-if="canViewApproveButton"
              :approved="approved"
              :disabled="currentDoc ? false : true"
            />
            <filter-button
              v-model="filterOption"
            />
            <guideline-button />
          </v-col>
          <v-spacer />
          <v-col>
            <pagination
              v-model="page"
              :length="total"
            />
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" md="9">
            <nuxt />
          </v-col>
          <v-col cols="12" md="3">
            <metadata-box
              v-if="currentDoc && !loading"
              :metadata="JSON.parse(currentDoc.meta)"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <bottom-navigator
      v-model="page"
      :length="total"
      class="d-flex d-sm-none"
    />
  </v-app>
</template>

<script>
import { mapActions, mapGetters, mapState, mapMutations } from 'vuex'
import BottomNavigator from '@/components/containers/annotation/BottomNavigator'
import GuidelineButton from '@/components/containers/annotation/GuidelineButton'
import MetadataBox from '@/components/organisms/annotation/MetadataBox'
import FilterButton from '@/components/containers/annotation/FilterButton'
import ApproveButton from '@/components/containers/annotation/ApproveButton'
import Pagination from '~/components/containers/annotation/Pagination'
import TheHeader from '~/components/organisms/layout/TheHeader'
import TheSideBar from '~/components/organisms/layout/TheSideBar'

export default {
  middleware: ['check-auth', 'auth', 'set-project'],

  components: {
    TheSideBar,
    TheHeader,
    BottomNavigator,
    Pagination,
    GuidelineButton,
    FilterButton,
    ApproveButton,
    MetadataBox
  },

  fetch() {
    this.getDocumentList({
      projectId: this.$route.params.id,
      limit: this.limit,
      offset: this.offset,
      q: this.$route.query.q,
      isChecked: this.filterOption,
      filterName: this.getFilterOption
    })
  },

  data() {
    return {
      drawerLeft: null,
      limit: 10
    }
  },

  computed: {
    ...mapGetters('projects', ['getLink', 'getCurrentUserRole', 'getFilterOption', 'canViewApproveButton']),
    ...mapState('documents', ['loading', 'total']),
    ...mapGetters('documents', ['currentDoc', 'approved']),
    page: {
      get() {
        return parseInt(this.$route.query.page, 10)
      },
      set(value) {
        this.$router.push({
          query: {
            isChecked: this.$route.query.isChecked,
            page: parseInt(value, 10),
            q: this.$route.query.q
          }
        })
      }
    },
    filterOption: {
      get() {
        return this.$route.query.isChecked
      },
      set(value) {
        this.$router.push({
          query: {
            isChecked: value,
            page: 1,
            q: this.$route.query.q
          }
        })
      }
    },
    offset() {
      return Math.floor((this.page - 1) / this.limit) * this.limit
    },
    current() {
      return (this.page - 1) % this.limit
    },
    searchOptions() {
      // a bit tricky technique to capture variables change simultaneously.
      // see https://github.com/vuejs/vue/issues/844#issuecomment-265315349
      return JSON.stringify({
        page: this.page,
        q: this.$route.query.q,
        isChecked: this.filterOption
      })
    }
  },

  watch: {
    total() {
      // To validate the range of page variable on reloading the annotation page.
      if (this.total !== 0 && this.page > this.total) {
        this.$router.push({
          path: `/projects/${this.$route.params.id}/`
        })
      }
    },
    offset() {
      this.$fetch()
    },
    filterOption() {
      this.page = 1
      this.$fetch()
    },
    current: {
      handler() {
        this.setCurrent(this.current)
      },
      immediate: true
    },
    searchOptions() {
      this.saveSearchOptions(JSON.parse(this.searchOptions))
    }
  },

  methods: {
    ...mapActions('documents', ['getDocumentList']),
    ...mapMutations('documents', ['setCurrent']),
    ...mapMutations('projects', ['saveSearchOptions'])
  }
}
</script>
