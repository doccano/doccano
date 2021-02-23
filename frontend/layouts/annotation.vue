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
      <v-snackbar
        v-model="snackbar"
      >
        {{ text }}
        <template v-slot:action="{ attrs }">
          <v-btn
            color="pink"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
      <v-container
        v-if="currentDoc && !loading"
        fluid
      >
        <v-row
          no-gutters
          class="d-none d-sm-flex"
        >
          <v-col>
            <approve-button
              v-if="canViewApproveButton"
              v-model="page"
              :length="total"
              :approved="approved"
              :disabled="currentDoc ? false : true"
            />
            <filter-button
              v-model="filterOption"
            />
            <guideline-button />
            <clear-annotations-button />
            <comment-button />
            <settings
              v-model="options"
              :errors="errors"
            />
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
              :metadata="JSON.parse(currentDoc.meta)"
            />
          </v-col>
        </v-row>
      </v-container>
      <v-container
        v-else
        fill-height
      >
      <v-layout align-center>
        <v-flex text-center>
          <h1 class="display-2 primary--text">
            Whoops, data is empty.
          </h1>
          <p>Please upload your dataset.</p>
        </v-flex>
      </v-layout>
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
import ClearAnnotationsButton from '@/components/containers/annotation/ClearAnnotationsButton.vue'
import GuidelineButton from '@/components/containers/annotation/GuidelineButton'
import MetadataBox from '@/components/organisms/annotation/MetadataBox'
import FilterButton from '@/components/containers/annotation/FilterButton'
import ApproveButton from '@/components/containers/annotation/ApproveButton'
import CommentButton from '../components/containers/comments/CommentButton.vue'
import Pagination from '~/components/containers/annotation/Pagination'
import TheHeader from '~/components/organisms/layout/TheHeader'
import TheSideBar from '~/components/organisms/layout/TheSideBar'
import Settings from '~/components/containers/annotation/Settings.vue'

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
    MetadataBox,
    ClearAnnotationsButton,
    CommentButton,
    Settings
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
      limit: 10,
      options: {
        onAutoLabeling: false
      },
      errors: {
        'autoLabelingConfig': ''
      },
      snackbar: false,
      text: ''
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
          path: this.localePath(`/projects/${this.$route.params.id}/`)
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
      async handler() {
        this.setCurrent(this.current)
        if (this.options.onAutoLabeling) {
          try {
            this.setLoading(true)
            await this.autoLabeling({ projectId: this.$route.params.id })
          } catch (e) {
            this.snackbar = true
            this.text = e.response.data.detail
          } finally {
            this.setLoading(false)
          }
        }
      },
      immediate: true
    },
    searchOptions() {
      this.saveSearchOptions(JSON.parse(this.searchOptions))
    },
    async "options.onAutoLabeling"(val) {
      if (val) {
        try {
          this.setLoading(true)
          await this.autoLabeling({ projectId: this.$route.params.id })
          this.errors.autoLabelingConfig = ''
        } catch (e) {
          this.errors.autoLabelingConfig = e.response.data.detail
          this.options.onAutoLabeling = false
        } finally {
          this.setLoading(false)
        }
      }
    }
  },

  methods: {
    ...mapActions('documents', ['getDocumentList', 'autoLabeling']),
    ...mapMutations('documents', ['setCurrent', 'setLoading']),
    ...mapMutations('projects', ['saveSearchOptions'])
  }
}
</script>
