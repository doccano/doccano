<template>
  <v-card>
    <v-card-title>
      <v-btn
        class="text-capitalize ms-2"
        color="primary"
        @click="goToAdd"
      >
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
    </v-card-title>

    <v-card-text>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="icons.mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
        style="margin-bottom: 1rem"
      />
      <v-progress-circular
        v-if="isLoading"
        class="ma-3"
        indeterminate
        color="primary"
      />

      <div v-if="!isLoading" class="d-flex justify-center">
        <div style="max-width: 800px; width: 100%;">
          <div
            v-for="item in items"
            :key="item.id"
            class="mb-4"
          >
            <v-card
              class="mx-auto"
              outlined
              elevation="2"
              rounded
            >
              <v-sheet
                color="primary"
                dark
                class="py-3 px-4 rounded-t-lg d-flex flex-column"
              >
                <div class="text-h6 font-weight-medium">
                  {{ item.user.username }}:
                  <span v-if="item.subject">
                    {{ item.subject }}
                  </span>
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
                <div
                  v-if="item.linkedAnnotations && item.linkedAnnotations.length"
                >
                  <v-divider class="my-2" />
                  <div
                    v-for="ann in item.linkedAnnotations"
                    :key="ann.uniqueId"
                    class="d-flex align-center"
                  >
                    <span
                      v-if="ann.text"
                      style="cursor: pointer;"
                      @click="viewAnnotation(item, ann)"
                    >
                      <strong>Annotation:</strong>
                      {{ ann.text }}
                      <span v-if="ann.label">
                        ({{ ann.label }})
                      </span>
                      <span v-if="ann.linkedBy">
                        — linked by <strong>{{ ann.linkedBy }}</strong>
                      </span>
                    </span>
                    <v-spacer />
                    <v-btn
                      icon
                      small
                      color="primary"
                      :disabled="user.role !== 'project_admin'"
                      @click="editAnnotation(item, ann)"
                    >
                      <v-icon>{{ icons.mdiPencil }}</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      small
                      :disabled="!canDeleteAnnotation(ann)"
                      color="red"
                      @click="removeAnnotation(item, ann)"
                    >
                      <v-icon>{{ icons.mdiTrashCan }}</v-icon>
                    </v-btn>
                  </div>
                </div>
              </v-card-text>

              <v-card-actions>
                <v-chip small>
                  {{ item.category }}
                </v-chip>
                <v-spacer />
                <v-btn
                  color="secondary"
                  small
                  @click="openLinkDialog(item)"
                >
                  Link Annotation
                </v-btn>
              </v-card-actions>
            </v-card>
          </div>

          <div v-if="items.length === 0">
            <p>No perspectives available.</p>
          </div>
        </div>
      </div>
    </v-card-text>

    <v-dialog v-model="dialogLink" persistent max-width="600px">
      <v-card>
        <v-card-title>
          Select a Dataset item to link its annotations
        </v-card-title>
        <v-card-text>
          <v-select
            v-model="selectedDataset"
            :items="datasetItems"
            :item-text="getDatasetLabel"
            item-value="id"
            label="Choose a dataset item"
            :item-disabled="isItemDisabled"
            dense
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="secondary"
            text
            @click="confirmLink"
            :disabled="!selectedDataset"
          >
            Confirm
          </v-btn>
          <v-btn text @click="closeLinkDialog">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogDelete" max-width="600px">
      <form-delete-perspective
        :selected="selected"
        @cancel="dialogDelete = false"
        @remove="remove"
      />
    </v-dialog>
  </v-card>
</template>

<script lang="ts">
// @ts-nocheck
import Vue from 'vue'
import axios from 'axios'
import { DataOptions } from 'vuetify/types'
import { mapGetters } from 'vuex'
import { mdiMagnify, mdiPencil, mdiTrashCan } from '@mdi/js'
import { getLinkToAnnotationPage } from '~/presenter/linkToAnnotationPage'

export default Vue.extend({
  name: 'PerspectivesTable',
  layout: 'project',
  data() {
    return {
      dialogDelete: false,
      dialogLink: false,
      selectedDataset: null,
      datasetItems: [] as any[],
      currentPerspective: null as any,
      selected: [] as any[],
      search: '',
      options: {
        page: 1,
        itemsPerPage: 10,
        sortBy: ['created_at'],
        sortDesc: [true]
      } as DataOptions,
      items: [] as any[],
      total: 0,
      isLoading: false,
      categoryTypes: [] as any[],
      icons: {
        mdiMagnify,
        mdiPencil,
        mdiTrashCan
      }
    }
  },
  computed: {
    ...mapGetters('projects', ['project']),
    ...mapGetters('auth', ['getUsername', 'getRolename']),
    user() {
      return {
        username: this.getUsername || 'Unknown',
        // Make sure getRolename returns "project_admin", "annotation_approver", or "annotator"
        role: this.getRolename || 'annotator'
      }
    },
    canDelete(): boolean {
      return this.selected.length > 0
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
    this.fetchCategoryTypes()
  },
  methods: {
    goToAdd() {
      const projectId = this.$route.params.id
      this.$router.push(
        this.localePath(`/projects/${projectId}/perspectives/add`)
      )
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
        offset: ((this.options.page ? this.options.page - 1 : 0) *
          this.options.itemsPerPage)
      }
      if (this.search) {
        query.q = this.search
      }
      this.isLoading = true
      axios.get(`/v1/projects/${projectId}/perspectives/`, { params: query })
        .then((_response: any) => {
          const data = _response.data
          const items = data.results || []
          const promises = items.map((item: any) => {
            if (typeof item.user === 'number') {
              return axios.get(`/v1/users/${item.user}/`)
                .then((_userResponse: any) => {
                  item.user = _userResponse.data
                })
                .catch(() => {
                  item.user = { username: 'N/A' }
                })
            }
            return Promise.resolve()
          })
          Promise.all(promises).then(() => {
            this.items = items
            this.total = data.count || items.length
          })
        })
        .catch((error: any) => {
          console.error(
            'Error fetching perspectives:',
            error.response || error.message
          )
        })
        .finally(() => {
          this.isLoading = false
        })
    },
    updateQuery() {
      this.fetchPerspectives()
    },
    timeAgo(dateStr: string): string {
      if (!dateStr) return 'N/A'
      const cleanDateStr = dateStr
        .replace(' ', 'T')
        .replace(/(\.\d{3})\d+/, '$1')
        .replace(/([+-]\d{2})(\d{2})$/, '$1:$2')
      const dateObj = new Date(cleanDateStr)
      if (isNaN(dateObj.getTime())) return 'N/A'
      const now = new Date()
      const diffMs = now.getTime() - dateObj.getTime()
      const diffSeconds = Math.floor(diffMs / 1000)
      if (diffSeconds < 60) return `${diffSeconds} seconds ago`
      const diffMinutes = Math.floor(diffSeconds / 60)
      if (diffMinutes < 60) return `${diffMinutes} minutes ago`
      const diffHours = Math.floor(diffMinutes / 60)
      if (diffHours < 24) return `${diffHours} hours ago`
      const diffDays = Math.floor(diffHours / 24)
      if (diffDays < 30) return `${diffDays} days ago`
      const diffMonths = Math.floor(diffDays / 30)
      if (diffMonths < 12) return `${diffMonths} months ago`
      const diffYears = Math.floor(diffMonths / 12)
      return `${diffYears} years ago`
    },
    formatTime(time: string): string {
      return this.timeAgo(time)
    },
    openLinkDialog(perspective: any) {
      this.currentPerspective = perspective
      this.dialogLink = true
      this.fetchDatasetItems()
    },
    fetchDatasetItems() {
      axios.get(
        `/v1/projects/${this.$route.params.id}/examples?limit=10&offset=0`
      )
        .then((_response: any) => {
          this.datasetItems = _response.data.results || []
          if (this.datasetItems.length > 0 && !this.selectedDataset) {
            const available = this.datasetItems.find(
              item => !this.isItemDisabled(item)
            )
            this.selectedDataset = available ? available.id : null
          }
        })
        .catch((error: any) => {
          console.error(
            'Error fetching dataset items:',
            error.response || error.message
          )
        })
    },
    fetchCategoryTypes() {
      const projectId = this.$route.params.id
      axios.get(`/v1/projects/${projectId}/category-types/`)
        .then((_response: any) => {
          this.categoryTypes =
            _response.data.results || _response.data || []
        })
        .catch((error: any) => {
          console.error(
            'Error fetching category types:',
            error.response || error.message
          )
        })
    },
    confirmLink() {
      if (!this.selectedDataset || !this.currentPerspective) {
        console.error(
          'selectedDataset or currentPerspective is not set.'
        )
        return
      }
      const datasetItem = this.datasetItems.find(
        item => item.id === this.selectedDataset
      )
      if (!datasetItem) {
        console.error('Dataset item not found.')
        return
      }
      const truncatedText = datasetItem.text.length > 50
        ? datasetItem.text.substring(0, 50) + '...'
        : datasetItem.text
      let label = ''
      let categoryId = null
      let fullCategory = null
      if (datasetItem.category && this.categoryTypes.length > 0) {
        let category
        if (typeof datasetItem.category === 'object') {
          category = this.categoryTypes.find(
            (cat: any) =>
              String(cat.id) === String(datasetItem.category.id)
          )
        } else {
          category = this.categoryTypes.find(
            (cat: any) =>
              String(cat.id) === String(datasetItem.category)
          )
        }
        if (category) {
          label = category.text
          categoryId = category.id
          fullCategory = { ...category }
        }
      }
      const annotation = {
        id: datasetItem.id,
        uniqueId: `${datasetItem.id}-${new Date().getTime()}`,
        text: truncatedText,
        label,
        categoryId,
        category: fullCategory,
        linkedBy: this.user.username
      }
      this.items.forEach((item: any, index: number) => {
        if (item.id === this.currentPerspective.id) {
          const duplicate = item.linkedAnnotations &&
            item.linkedAnnotations.find(
              (ann: any) => ann.id === datasetItem.id
            )
          if (duplicate) {
            console.warn(
              `Annotation for dataset item ${datasetItem.id} is already linked.`
            )
            return
          }
          const updatedAnnotations = item.linkedAnnotations
            ? [...item.linkedAnnotations, annotation]
            : [annotation]
          this.$set(this.items, index, {
            ...item,
            linkedAnnotations: updatedAnnotations
          })
          const projectId = this.$route.params.id
          axios.patch(
            `/v1/projects/${projectId}/perspectives/${this.currentPerspective.id}/`,
            { linkedAnnotations: updatedAnnotations }
          )
            .then((_response: any) => {
              this.fetchPerspectives()
            })
            .catch((error: any) => {
              console.error(
                "Error updating perspective:",
                error.response || error.message
              )
            })
        }
      })
      this.closeLinkDialog()
    },
    closeLinkDialog() {
      this.dialogLink = false
      this.selectedDataset = null
      this.currentPerspective = null
    },
    getDatasetLabel(item: any): string {
      const snippet = item.text
        ? item.text.substring(0, 50) +
          (item.text.length > 50 ? '...' : '')
        : ''
      const timeLabel = item.created_at
        ? this.formatTime(item.created_at)
        : item.upload_name || 'Unknown time'
      return `${snippet} (${timeLabel})`
    },
    isItemDisabled(item: any) {
      if (!this.currentPerspective || !this.currentPerspective.linkedAnnotations) {
        return false
      }
      return this.currentPerspective.linkedAnnotations.some(
        (ann: any) => ann.id === item.id
      )
    },
    editAnnotation(item: any, ann: any) {
      if (this.user.role !== 'project_admin') {
        console.error("Only project admins can edit linked annotations.")
        return
      }
      const projectId = this.$route.params.id
      const found = item.linkedAnnotations.findIndex((a: any) => a.uniqueId === ann.uniqueId)
      const page = (found !== -1 ? found : 0) + 1
      const link = getLinkToAnnotationPage(projectId, this.project.projectType)
      this.$router.push({
        path: this.localePath(link),
        query: { page: page.toString() }
      })
    },
    canDeleteAnnotation(annotation: any): boolean {
      const role = this.user.role
      if (role === 'project_admin') {
        return true
      } else if (role === 'annotation_approver') {
        return (
          annotation.linkedBy === this.user.username ||
          annotation.linkedByRole === 'annotator'
        )
      } else if (role === 'annotator') {
        return annotation.linkedBy === this.user.username
      }
      return false
    },
    removeAnnotation(item: any, ann: any) {
      if (!this.canDeleteAnnotation(ann)) {
        console.error("You do not have permission to delete this annotation.")
        return
      }
      const updatedAnnotations = item.linkedAnnotations.filter(
        (a: any) => a.uniqueId !== ann.uniqueId
      )
      const index = this.items.findIndex((it: any) => it.id === item.id)
      if (index !== -1) {
        this.$set(this.items, index, { 
          ...item,
          linkedAnnotations: updatedAnnotations
        })
      }
      axios.patch(
        `/v1/projects/${this.$route.params.id}/perspectives/${item.id}/`,
        { linkedAnnotations: updatedAnnotations }
      )
        .then((_response: any) => {
          this.fetchPerspectives()
        })
        .catch((error: any) => {
          console.error(
            "Error removing annotation:",
            error.response || error.message
          )
        })
    },
    viewAnnotation(item: any, ann: any) {
      const projectId = this.$route.params.id
      const limit = 10
      let index = 0
      if (item.linkedAnnotations && item.linkedAnnotations.length) {
        const found = item.linkedAnnotations.findIndex(
          (a: any) => a.uniqueId === ann.uniqueId
        )
        index = found !== -1 ? found : 0
      }
      const offset = index * limit
      this.$router.push({
        path: this.localePath(`/projects/${projectId}/dataset`),
        query: {
          limit: limit.toString(),
          offset: offset.toString()
        }
      })
    }
  },
})
</script>

<style scoped>
</style>