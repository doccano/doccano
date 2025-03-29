<template>
  <v-card>
    <v-card-title>
      <v-btn class="text-capitalize ms-2" color="primary" @click="goToAdd">
        {{ $t('generic.add') }}
      </v-btn>
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete" max-width="600px">
        <form-delete-perspective
          :selected="selected"
          @cancel="dialogDelete = false"
          @remove="remove"
        />
      </v-dialog>
    </v-card-title>

    <v-card-text>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
        style="margin-bottom: 1rem"
      />
      <v-progress-circular
        v-if="isLoading"
        indeterminate
        color="primary"
        class="ma-3"
      />

      <div class="d-flex justify-center" v-if="!isLoading">
        <div style="max-width: 800px; width: 100%;">
          <div v-for="item in items" :key="item.id" class="mb-4">
            <v-card class="mx-auto" outlined elevation="2" rounded>
              <!-- Header bar using v-sheet: shows "username: subject" -->
              <v-sheet color="primary" dark class="py-3 px-4 rounded-t-lg d-flex flex-column">
                <div class="text-h6 font-weight-medium">
                  {{ item.user.username }}:<span v-if="item.subject"> {{ item.subject }}</span>
                </div>
                <div class="text-body-2">
                  {{ formatTime(item.created_at) }}
                  <span v-if="item.updated_at !== item.created_at">
                    &bull; Updated: {{ formatTime(item.updated_at) }}
                  </span>
                </div>
              </v-sheet>

              <v-card-text>
                <div>
                  {{ item.text }}
                </div>
              </v-card-text>

              <v-card-actions>
                <v-chip small>{{ item.category }}</v-chip>
              </v-card-actions>
            </v-card>
          </div>

          <div v-if="items.length === 0">
            <p>No perspectives available.</p>
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import Vue from 'vue'
import axios from 'axios'
import { DataOptions } from 'vuetify/types'

export default Vue.extend({
  name: 'PerspectivesTable',
  layout: 'project',
  data() {
    return {
      dialogDelete: false,
      selected: [] as any[],
      search: '',
      options: {
        page: 1,
        itemsPerPage: 10,
        sortBy: ['created_at'],
        sortDesc: [true],
      } as DataOptions,
      items: [] as any[],
      total: 0,
      isLoading: false,
      mdiMagnify,
    }
  },
  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    }
  },
  methods: {
    goToAdd() {
      const projectId = this.$route.params.id
      this.$router.push(this.localePath(`/projects/${projectId}/perspectives/add`))
    },
    remove() {
      this.$emit('remove', this.selected)
      this.dialogDelete = false
      this.selected = []
    },
    fetchPerspectives() {
      const projectId = this.$route.params.id
      const query: any = {
        limit: this.options.itemsPerPage,
        offset: ((this.options.page ? this.options.page - 1 : 0) * this.options.itemsPerPage)
      }
      if (this.search) {
        query.q = this.search
      }
      this.isLoading = true
      axios.get(`/v1/projects/${projectId}/perspectives/`, { params: query })
        .then((response: any) => {
          console.log('API Response:', response.data)
          const data = response.data
          const items = data.results || []
          // For each perspective, if the user is a number, fetch user details.
          const promises = items.map((item: any) => {
            if (typeof item.user === 'number') {
              return axios.get(`/v1/users/${item.user}/`)
                .then((userResponse: any) => {
                  item.user = userResponse.data
                })
                .catch(() => {
                  item.user = { username: 'N/A' }
                })
            } else {
              return Promise.resolve()
            }
          })
          Promise.all(promises).then(() => {
            console.log('Processed Items:', items)
            this.items = items
            this.total = data.count || items.length
          })
        })
        .catch((error: any) => {
          console.error('Error fetching perspectives:', error.response || error.message)
        })
        .finally(() => {
          this.isLoading = false
        })
    },
    updateQuery() {
      this.fetchPerspectives()
    },
    // Simple relative time formatter.
    timeAgo(dateStr: string): string {
      if (!dateStr) return 'N/A'
      const dateObj = new Date(dateStr)
      const now = new Date()
      const diffMs = now.valueOf() - dateObj.valueOf()
      const diffSeconds = Math.floor(diffMs / 1000)
      if (diffSeconds < 60) return `${diffSeconds} seconds ago`
      const diffMinutes = Math.floor(diffSeconds / 60)
      if (diffMinutes < 60) return `${diffMinutes} minutes ago`
      const diffHours = Math.floor(diffMinutes / 60)
      if (diffHours < 24) return `${diffHours} hours ago`
      const diffDays = Math.floor(diffHours / 24)
      if (diffDays < 7) return `${diffDays} days ago`
      if (diffDays < 30) return `${diffDays} days ago`
      const diffMonths = Math.floor(diffDays / 30)
      if (diffMonths < 12) return `${diffMonths} months ago`
      const diffYears = Math.floor(diffMonths / 12)
      return `${diffYears} years ago`
    },
    formatTime(time: string): string {
      return this.timeAgo(time)
    }
  },
  watch: {
    options: {
      handler() {
        this.updateQuery()
      },
      deep: true
    },
    search() {
      this.options.page = 1
      this.updateQuery()
    }
  },
  mounted() {
    this.fetchPerspectives()
  }
})
</script>

<style scoped>
</style>