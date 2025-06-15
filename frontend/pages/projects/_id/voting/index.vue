<template>
  <v-container fluid>
        <!-- Database Error Alert - Always visible when database is down -->
        <v-alert
      v-if="!isDatabaseHealthy"
      ref="databaseAlert"
          type="error"
          prominent
          class="mb-4"
        >
      <v-row align="center">
        <v-col class="grow">
          <div class="title">De momento, a base de dados não se encontra disponível. Por favor, tente mais tarde.</div>
        </v-col>
        <v-col class="shrink">
          <v-icon size="48">mdi-database-alert</v-icon>
      </v-col>
    </v-row>
    </v-alert>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2>Voting</h2>
          </v-card-title>

          <v-card-text>
            <!-- Header with Create Button -->
            <div class="d-flex justify-space-between align-center mb-6">
              <div>
                <p class="text-body-2 grey--text mb-0">
                </p>
              </div>
              <v-btn
                :color="canConfigureVoting ? 'primary' : 'grey'"
                :disabled="!canConfigureVoting"
                @click="goToConfiguration"
              >
                <v-icon left>{{ mdiPlus }}</v-icon>
                Create New Voting
              </v-btn>
            </div>

            <!-- Configurations List -->
            <div v-if="votingConfigurations.length > 0">
              <v-expansion-panels multiple>
                <v-expansion-panel
                  v-for="(config, index) in votingConfigurations"
                  :key="config.id"
                >
                  <v-expansion-panel-header>
                    <div class="d-flex align-center">
                      <v-icon class="mr-3" color="primary">{{ mdiVote }}</v-icon>
                      <div>
                        <div class="font-weight-bold">{{ config.name }}</div>
                        <div class="text-body-2 grey--text">
                          {{ formatDate(config.startDate) }} - {{ formatDate(config.endDate) }} | 
                          {{ config.annotationRules.length }} rules
                        </div>
                      </div>
                      <v-spacer />
                      <v-chip
                        :color="getVotingMethodColor(config.votingMethod)"
                        dark
                        small
                        class="mr-2"
                      >
                        {{ getVotingMethodText(config.votingMethod) }}
                      </v-chip>
                    </div>
                  </v-expansion-panel-header>

                  <v-expansion-panel-content>
                    <v-card flat>
                      <v-card-text class="pa-0 pt-4">
                        <v-row>
                          <!-- Basic Information -->
                          <v-col cols="12" md="6">
                            <h4 class="text-h6 mb-3">Basic Information</h4>
                            <div class="mb-2">
                              <strong>Description:</strong> {{ config.description }}
                            </div>
                            <div class="mb-2">
                              <strong>Period:</strong> {{ formatDate(config.startDate) }} - {{ formatDate(config.endDate) }}
                            </div>
                            <div class="mb-2">
                              <strong>Time:</strong> {{ config.startTime }} - {{ config.endTime }}
                            </div>
                            <div class="mb-2">
                              <strong>Created:</strong> {{ formatDateTime(config.createdAt) }}
                            </div>
                          </v-col>

                          <!-- Voting Method -->
                          <v-col cols="12" md="6">
                            <h4 class="text-h6 mb-3">Voting Method</h4>
                            <v-chip
                              :color="getVotingMethodColor(config.votingMethod)"
                              dark
                              class="mb-2"
                            >
                              {{ getVotingMethodText(config.votingMethod) }}
                            </v-chip>
                            <p class="text-body-2 grey--text mt-2">
                              {{ getVotingMethodDescription(config.votingMethod) }}
                            </p>
                          </v-col>

                          <!-- Annotation Rules -->
                          <v-col cols="12">
                            <h4 class="text-h6 mb-3">Annotation Rules ({{ config.annotationRules.length }})</h4>
                            <v-row>
                              <v-col
                                v-for="(rule, ruleIndex) in config.annotationRules"
                                :key="ruleIndex"
                                cols="12"
                                md="6"
                              >
                                <v-card outlined class="mb-2">
                                  <v-card-text class="py-3">
                                    <div class="font-weight-bold text-subtitle-2 mb-1">
                                      {{ rule.name }}
                                    </div>
                                    <div class="text-body-2 grey--text">
                                      {{ rule.description }}
                                    </div>
                                  </v-card-text>
                                </v-card>
                              </v-col>
                            </v-row>
                          </v-col>
                        </v-row>

                        <!-- Actions -->
                        <v-divider class="my-4" />
                        <div class="d-flex justify-space-between">
                          <v-btn
                            color="primary"
                            outlined
                            @click="editConfiguration(config)"
                          >
                            <v-icon left>{{ mdiPencil }}</v-icon>
                            Edit Configuration
                          </v-btn>
                          
                          <v-btn
                            color="error"
                            outlined
                            @click="deleteConfiguration(config, index)"
                          >
                            <v-icon left>{{ mdiDelete }}</v-icon>
                            Delete
                          </v-btn>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center pa-12">
              <v-icon size="120" color="grey lighten-1">
                {{ mdiVote }}
              </v-icon>
              <h3 class="text-h5 grey--text text--darken-1 mt-4">
                No Voting Configurations
              </h3>
              <p class="text-body-1 grey--text mt-2">
                Create your first voting configuration to get started.
              </p>
            </div>

            <!-- Status message -->
            <div class="mt-6 text-center">
              <v-alert
                v-if="!hasDiscussions"
                type="info"
                text
                class="mb-0"
                :icon="false"
              >
                <strong>No discussions created yet.</strong><br>
                Create a discussion first to enable voting configuration.
                <br><br>
                <v-btn
                  color="primary"
                  small
                  outlined
                  @click="goToDiscussions"
                >
                  Go to Discussions
                </v-btn>
              </v-alert>
              
              <v-alert
                v-else-if="openDiscussions.length > 0"
                type="warning"
                text
                class="mb-0"
                :icon="false"
              >
                <strong>{{ openDiscussions.length }} discussion(s) currently open.</strong><br>
                Close all discussions to enable voting configuration.
                <br><br>
                <v-btn
                  color="orange"
                  small
                  outlined
                  @click="goToDiscussions"
                >
                  Manage Discussions
                </v-btn>
              </v-alert>
              
              <v-alert
                v-else-if="votingConfigurations.length === 0"
                type="success"
                text
                class="mb-0"
                :icon="false"
              >
                <strong>All discussions are closed.</strong><br>
                You can now configure voting for this project.
              </v-alert>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Confirmation Dialog for Active Voting -->
    <v-dialog v-model="showActiveVotingDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title class="text-h5">
          <v-icon left color="warning">{{ mdiAlert }}</v-icon>
          Active Voting Found
        </v-card-title>
        
        <v-card-text>
          <p class="mb-3">
            <strong>There is currently an active voting:</strong>
          </p>
          <v-card outlined class="mb-3">
            <v-card-text class="py-2">
              <div class="font-weight-bold">{{ activeVotingConfig?.name }}</div>
              <div class="text-body-2 grey--text">
                {{ formatDate(activeVotingConfig?.startDate) }} - {{ formatDate(activeVotingConfig?.endDate) }}
              </div>
            </v-card-text>
          </v-card>
          <p class="mb-0">
            Only one voting can be active at a time. Do you want to terminate the previous voting early and configure a new one?
          </p>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn
            text
            @click="cancelNewVoting"
          >
            Cancel
          </v-btn>
          <v-btn
            color="warning"
            @click="terminateAndCreateNew"
          >
            Terminate and Create New
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import {
  mdiVote,
  mdiCog,
  mdiCheckCircle,
  mdiPencil,
  mdiPlus,
  mdiDelete,
  mdiAlert
} from '@mdi/js'
import { databaseHealthMixin } from '@/mixins/databaseHealthMixin'

export default {
  mixins: [databaseHealthMixin],
  layout: 'project',

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      mdiVote,
      mdiCog,
      mdiCheckCircle,
      mdiPencil,
      mdiPlus,
      mdiDelete,
      mdiAlert,
      discussions: [],
      votingConfigurations: [],
      showActiveVotingDialog: false,
      activeVotingConfig: null
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      await this.$services.project.findById(this.$route.params.id)
      
      // Fetch discussions to check their status
      const discussionsRes = await this.$axios.get(`/v1/projects/${this.$route.params.id}/discussions/`)
      this.discussions = Array.isArray(discussionsRes.data?.results) ? discussionsRes.data.results : []
      
      // Load voting configurations from localStorage
      const savedConfigs = localStorage.getItem(`voting_configs_${this.$route.params.id}`)
      if (savedConfigs) {
        this.votingConfigurations = JSON.parse(savedConfigs)
      }
    } catch(e) {
      throw new Error(e.response.data.detail)
    } finally {
      this.isLoading = false
    }
  },

  head() {
    return {
      title: 'Voting'
    }
  },

  watch: {
    isDatabaseHealthy(newValue, oldValue) {
      // Se a base de dados ficou indisponível (mudou de true para false)
      if (oldValue === true && newValue === false) {
        // Aguarda o próximo tick para garantir que o alerta foi renderizado
        this.$nextTick(() => {
          // Faz scroll para o topo da página para mostrar o alerta
          window.scrollTo({
            top: 0,
            behavior: 'smooth'
          })
        })
      }
    }
  },

  computed: {
    project() {
      return this.$store.getters['projects/project']
    },
    
    isProjectAdmin() {
      return this.$store.getters['projects/isProjectAdmin']
    },

    openDiscussions() {
      const todayString = new Date().toISOString().substr(0, 10)
      return this.discussions.filter(d => 
        d.start_date <= todayString && d.end_date > todayString
      )
    },

    hasDiscussions() {
      return this.discussions.length > 0
    },

    canConfigureVoting() {
      // Button is enabled only if:
      // 1. There are discussions created AND
      // 2. No discussions are currently open (all are closed)
      return this.hasDiscussions && this.openDiscussions.length === 0
    }
  },

  methods: {
    goToConfiguration() {
      // Check if there's an active voting configuration
      const activeVoting = this.getActiveVotingConfiguration()
      
      if (activeVoting) {
        this.activeVotingConfig = activeVoting
        this.showActiveVotingDialog = true
      } else {
        this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting/configure`))
      }
    },

    getActiveVotingConfiguration() {
      const now = new Date()
      const currentDate = now.toISOString().substr(0, 10)
      const currentTime = now.toTimeString().substr(0, 5)

      return this.votingConfigurations.find(config => {
        const startDate = config.startDate
        const endDate = config.endDate
        const startTime = config.startTime
        const endTime = config.endTime

        // Check if current date is within the voting period
        if (currentDate < startDate || currentDate > endDate) {
          return false
        }

        // If it's the start date, check if current time is after start time
        if (currentDate === startDate && currentTime < startTime) {
          return false
        }

        // If it's the end date, check if current time is before end time
        if (currentDate === endDate && currentTime >= endTime) {
          return false
        }

        return true
      })
    },

    cancelNewVoting() {
      this.showActiveVotingDialog = false
      this.activeVotingConfig = null
    },

    terminateAndCreateNew() {
      if (this.activeVotingConfig) {
        // Find the index of the active voting configuration
        const configIndex = this.votingConfigurations.findIndex(
          config => config.id === this.activeVotingConfig.id
        )

        if (configIndex !== -1) {
          // Terminate the active voting by setting end date and time to now
          const now = new Date()
          this.votingConfigurations[configIndex].endDate = now.toISOString().substr(0, 10)
          this.votingConfigurations[configIndex].endTime = now.toTimeString().substr(0, 5)
          
          // Save to localStorage
          localStorage.setItem(
            `voting_configs_${this.$route.params.id}`, 
            JSON.stringify(this.votingConfigurations)
          )
        }
      }

      // Close dialog and navigate to configuration
      this.showActiveVotingDialog = false
      this.activeVotingConfig = null
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting/configure`))
    },

    editConfiguration(config) {
      // Store the configuration ID to edit in session storage
      sessionStorage.setItem('editingConfigId', config.id.toString())
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting/configure`))
    },

    async deleteConfiguration(config, index) {
      const confirmed = await this.$confirm(`Are you sure you want to delete the voting configuration "${config.name}"?`, {
        title: 'Delete Configuration',
        buttonTrueText: 'Delete',
        buttonFalseText: 'Cancel',
        color: 'error'
      })

      if (confirmed) {
        this.votingConfigurations.splice(index, 1)
        localStorage.setItem(`voting_configs_${this.$route.params.id}`, JSON.stringify(this.votingConfigurations))
      }
    },

    goToDiscussions() {
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/discussions`))
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },

    formatDateTime(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getVotingMethodText(method) {
      const methods = {
        'approve_only': 'Approve Only',
        'disapprove_only': 'Disapprove Only',
        'approve_disapprove': 'Approve or Disapprove'
      }
      return methods[method] || method
    },

    getVotingMethodColor(method) {
      const colors = {
        'approve_only': 'success',
        'disapprove_only': 'error',
        'approve_disapprove': 'primary'
      }
      return colors[method] || 'grey'
    },

    getVotingMethodDescription(method) {
      const descriptions = {
        'approve_only': 'Annotators can only approve rules they support',
        'disapprove_only': 'Annotators can only reject rules they oppose',
        'approve_disapprove': 'Annotators must vote on every rule'
      }
      return descriptions[method] || ''
    }
  }
}
</script> 