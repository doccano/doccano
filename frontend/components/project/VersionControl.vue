<template>
  <v-container>
    <v-row>
      <!-- Status Card -->
      <v-col cols="12" md="6">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon :color="(project.isOpen !== undefined ? project.isOpen : true) ? 'green' : 'red'" class="mr-2">
              {{ (project.isOpen !== undefined ? project.isOpen : true) ? 'mdi-lock-open' : 'mdi-lock' }}
            </v-icon>
            <span>Project Status</span>
          </v-card-title>
          <v-card-text>
            <v-row class="mb-2">
              <v-col cols="6">
                <div class="text-caption text--secondary">Status</div>
                <v-chip 
                  :color="(project.isOpen !== undefined ? project.isOpen : true) ? 'green' : 'red'" 
                  dark 
                  small
                >
                  {{ (project.isOpen !== undefined ? project.isOpen : true) ? 'Open' : 'Closed' }}
                </v-chip>
              </v-col>
              <v-col cols="6">
                <div class="text-caption text--secondary">Current Version</div>
                <div class="text-h6">{{ project.currentVersion || 1 }}</div>
              </v-col>
            </v-row>
            <v-row class="mb-2">
              <v-col cols="12">
                <div class="text-caption text--secondary">Discrepancy Threshold</div>
                <div class="text-h6">{{ project.label_discrepancy_threshold }}%</div>
              </v-col>
            </v-row>
            
            <!-- Version > 1 - Show discrepancy stats -->
            <v-row v-if="(project.currentVersion || 1) > 1 && versionStatus" class="mb-2">
              <v-col cols="12">
                <div class="text-caption text--secondary">Discrepant Examples</div>
                <div class="text-h6">{{ versionStatus.discrepant_examples_count || 0 }}</div>
                <div class="text-caption">Only these examples can be annotated</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Actions Card -->
      <v-col cols="12" md="6">
        <v-card class="pa-4" elevation="2">
          <v-card-title>
            <v-icon class="mr-2">mdi-cog</v-icon>
            <span>Version Control</span>
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <div class="text-caption text--secondary mb-2">Current Phase</div>
              <v-alert 
                :type="(project.isOpen !== undefined ? project.isOpen : true) ? 'info' : 'warning'" 
                dense 
                outlined 
                class="mb-3"
              >
                <div v-if="project.isOpen !== undefined ? project.isOpen : true">
                  <strong>Annotation Phase</strong><br>
                  Users can annotate examples
                  <span v-if="(project.currentVersion || 1) > 1">
                    (only discrepant examples)
                  </span>
                </div>
                <div v-else>
                  <strong>Discussion & Voting Phase</strong><br>
                  Users can discuss criteria and vote on rules
                </div>
              </v-alert>
            </div>
            
            <v-btn 
              v-if="project.isOpen !== undefined ? project.isOpen : true"
              @click="closeProject"
              :loading="loading"
              color="warning"
              block
              class="mb-2"
            >
              <v-icon left>mdi-lock</v-icon>
              Close Project
            </v-btn>
            
            <v-btn 
              v-else
              @click="reopenProject"
              :loading="loading"
              color="success"
              block
              class="mb-2"
            >
              <v-icon left>mdi-lock-open</v-icon>
              Reopen Project (Version {{ (project.currentVersion || 1) + 1 }})
            </v-btn>
            
            <div class="text-caption text--secondary mt-2">
              <div v-if="project.isOpen !== undefined ? project.isOpen : true">
                Closing will prevent annotations and enable discussions/voting
              </div>
              <div v-else>
                Reopening will create a new version and allow annotations
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Version History -->
    <v-row v-if="versionStatus && versionStatus.versions_history.length > 0">
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <v-card-title>
            <v-icon class="mr-2">mdi-history</v-icon>
            <span>Version History</span>
          </v-card-title>
          <v-card-text>
            <v-timeline dense>
              <v-timeline-item
                v-for="version in versionStatus.versions_history"
                :key="version.version"
                :color="version.version === (project.currentVersion || 1) ? 'primary' : 'grey'"
                small
              >
                <v-row class="pt-1">
                  <v-col cols="3">
                    <strong>Version {{ version.version }}</strong>
                  </v-col>
                  <v-col cols="4">
                    <div class="text-caption text--secondary">Created by</div>
                    <div>{{ version.created_by || 'System' }}</div>
                  </v-col>
                  <v-col cols="5">
                    <div class="text-caption text--secondary">Created at</div>
                    <div>{{ formatDate(version.created_at) }}</div>
                  </v-col>
                </v-row>
                <div v-if="version.notes" class="mt-2">
                  <div class="text-caption text--secondary">Notes</div>
                  <div>{{ version.notes }}</div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Snackbar for notifications -->
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      timeout="3000"
      top
    >
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn
          color="white"
          text
          v-bind="attrs"
          @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'

export default Vue.extend({
  name: 'VersionControl',

  data() {
    return {
      loading: false,
      versionStatus: null as any,
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success'
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    
    projectId(): string {
      return this.$route.params.id
    }
  },

  async mounted() {
    await this.loadVersionStatus()
  },

  methods: {
    async loadVersionStatus() {
      try {
        this.versionStatus = await this.$repositories.project.getVersionStatus(this.projectId)
      } catch (error) {
        console.error('Error loading version status:', error)
        this.showSnackbar('Error loading version status', 'error')
      }
    },

    async closeProject() {
      try {
        this.loading = true
        await this.$repositories.project.closeProject(this.projectId)
        
        // Update project in store
        await this.$store.dispatch('projects/setCurrentProject', this.projectId)
        
        // Reload version status
        await this.loadVersionStatus()
        
        this.showSnackbar('Project closed successfully', 'success')
      } catch (error) {
        console.error('Error closing project:', error)
        this.showSnackbar('Error closing project', 'error')
      } finally {
        this.loading = false
      }
    },

    async reopenProject() {
      try {
        this.loading = true
        const response = await this.$repositories.project.reopenProject(this.projectId)
        
        // Update project in store
        await this.$store.dispatch('projects/setCurrentProject', this.projectId)
        
        // Reload version status
        await this.loadVersionStatus()
        
        this.showSnackbar(`Project reopened in version ${response.project.current_version}`, 'success')
      } catch (error) {
        console.error('Error reopening project:', error)
        this.showSnackbar('Error reopening project', 'error')
      } finally {
        this.loading = false
      }
    },

    showSnackbar(text: string, color: string = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },

    formatDate(dateString: string): string {
      return new Date(dateString).toLocaleString()
    }
  }
})
</script>

<style scoped>
.v-timeline-item {
  padding-bottom: 16px;
}
</style> 