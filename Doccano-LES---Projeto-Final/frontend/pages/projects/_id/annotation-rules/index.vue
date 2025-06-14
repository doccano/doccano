<template>
  <v-container>
    <v-card>
      <v-card-title>Annotation Rules</v-card-title>
      <v-card-subtitle>
        Users can vote on annotation rules for the project.
      </v-card-subtitle>
      <v-card-text>
        <v-row justify="end" class="mb-4">
          <v-col cols="auto">
            <v-btn 
              color="primary" 
              class="text-capitalize"
              :disabled="!isDiscussionEnded || hasActiveVoting" 
              @click="showVotingConfig = true"
            >
              <v-icon left>
                {{ mdiPoll }}
              </v-icon>
              Configure new voting
            </v-btn>
          </v-col>
        </v-row>
        
        <v-alert
          v-if="!isDiscussionEnded"
          type="info"
          outlined
        >
          Before configuring a vote, it is necessary that the discussion about discrepancies is finalized.
          Go to the <router-link :to="`/projects/${projectId}/discrepancies`">discrepancies</router-link> page to participate in the discussion.
        </v-alert>
        
        <v-alert
          v-else-if="hasActiveVoting"
          type="warning"
          outlined
        >
          There is already an ongoing voting. Wait for the current voting to end before configuring a new one.
        </v-alert>
        
        <v-alert
          v-else
          type="success"
          outlined
        >
          The discussion has ended. You can now configure a new voting.
        </v-alert>
        
        <!-- Ongoing voting -->
        <v-card 
          v-if="activeVoting"
          outlined
          class="mt-4"
        >
          <v-card-title class="subtitle-1">
            Ongoing Voting
            <v-btn 
              icon
              small
              text
              min-width="20"
              min-height="20"
              style="border: 1px solid #ddd; margin-left: 8px; width: 20px; height: 20px; padding: 0;"
              @click="simulateDatabaseError = true"
            ></v-btn>
            <v-btn 
              v-if="simulateDatabaseError"
              icon
              small
              text
              min-width="20"
              min-height="20"
              style="border: 1px solid #ddd; margin-left: 4px; width: 20px; height: 20px; padding: 0; background-color: #f0f0f0;"
              @click="simulateDatabaseError = false"
            ></v-btn>
            <v-spacer></v-spacer>
            <v-btn 
              v-if="isAdmin" 
              color="error" 
              small 
              outlined
              @click="confirmEndVoting = true"
            >
              <v-icon left small>mdi-timer-off</v-icon>
              End voting
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-calendar-start</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>Start</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDate(activeVoting.startDate) }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
              
              <v-col cols="12" sm="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-calendar-end</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>End</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDate(activeVoting.endDate) }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
            
            <div class="my-4">
              <div class="font-weight-medium mb-2">Description:</div>
              <div>{{ activeVoting.description }}</div>
            </div>
            
            <!-- Filters section -->
            <v-card outlined class="mb-4">
              <v-card-title class="subtitle-2">
                <v-icon left small>mdi-filter</v-icon>
                Filters
                <v-spacer></v-spacer>
                <v-btn
                  x-small
                  text
                  color="primary"
                  @click="resetFilters"
                >
                  Reset filters
                </v-btn>
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" sm="4">
                    <v-text-field
                      v-model="filters.keyword"
                      label="Search by keyword"
                      dense
                      outlined
                      clearable
                      prepend-inner-icon="mdi-magnify"
                      hide-details
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <v-select
                      v-model="filters.voteStatus"
                      :items="voteStatusOptions"
                      label="Vote status"
                      dense
                      outlined
                      clearable
                      hide-details
                    ></v-select>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <v-select
                      v-model="filters.voteResult"
                      :items="voteResultOptions"
                      label="Current result"
                      dense
                      outlined
                      clearable
                      hide-details
                    ></v-select>
                  </v-col>
                </v-row>
                <v-row class="mt-2">
                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="filters.category"
                      :items="getCategoryOptions"
                      label="Category"
                      dense
                      outlined
                      clearable
                      hide-details
                    ></v-select>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="filters.sortBy"
                      :items="sortOptions"
                      label="Sort by"
                      dense
                      outlined
                      hide-details
                    ></v-select>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
            
            <div class="my-4">
              <div class="font-weight-medium mb-2 d-flex align-center">
                Rules in voting:
                <v-chip class="ml-2" x-small>{{ filteredRules.length }} of {{ activeVoting.rules.length }}</v-chip>
              </div>
              <v-list>
                <v-list-item
                  v-for="ruleId in filteredRules"
                  :key="ruleId"
                >
                  <v-list-item-content>
                    <v-list-item-title class="d-flex align-center">
                      {{ getRuleName(ruleId) }}
                      <v-chip
                        x-small
                        class="ml-2"
                        :color="hasVotedForRule(ruleId) ? 'info' : 'grey'"
                        :text-color="hasVotedForRule(ruleId) ? 'white' : ''"
                      >
                        <v-icon v-if="hasVotedForRule(ruleId)" x-small left>mdi-check</v-icon>
                        {{ hasVotedForRule(ruleId) ? 'Voted' : 'Not voted' }}
                      </v-chip>
                      <v-chip
                        v-if="hasVotedForRule(ruleId) && !isAdmin"
                        x-small
                        class="ml-2"
                        color="primary"
                      >
                        Your vote: {{ getUserVoteForRule(ruleId) === 'aprovar' ? 'Approve' : 'Reject' }}
                      </v-chip>
                      <v-chip
                        v-if="ruleCategory(ruleId)"
                        x-small
                        class="ml-2"
                        :color="ruleCategory(ruleId) ? 'purple' : 'grey'"
                      >
                        {{ ruleCategory(ruleId) }}
                      </v-chip>
                    </v-list-item-title>
                    <v-list-item-subtitle>{{ getRuleDescription(ruleId) }}</v-list-item-subtitle>
                    
                    <div class="mt-2">
                      <v-chip 
                        small 
                        color="success" 
                        class="mr-2" 
                        outlined
                      >
                        <v-icon left x-small>mdi-thumb-up</v-icon>
                        Approvals: {{ ruleVotes(ruleId).aprovar }}
                      </v-chip>
                      <v-chip 
                        small 
                        color="error" 
                        outlined
                      >
                        <v-icon left x-small>mdi-thumb-down</v-icon>
                        Rejections: {{ ruleVotes(ruleId).rejeitar }}
                      </v-chip>
                    </div>
                  </v-list-item-content>
                  
                  <v-list-item-action class="d-flex">
                    <v-btn 
                      color="success"
                      text
                      :disabled="hasVotedForRule(ruleId) || isAdmin"
                      class="mr-2"
                      @click="voteForRule(ruleId, 'aprovar')"
                    >
                      <v-icon left small>mdi-thumb-up</v-icon>
                      Approve
                    </v-btn>
                    <v-btn 
                      color="error"
                      text
                      :disabled="hasVotedForRule(ruleId) || isAdmin"
                      @click="voteForRule(ruleId, 'rejeitar')"
                    >
                      <v-icon left small>mdi-thumb-down</v-icon>
                      Reject
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list>

              <div v-if="filteredRules.length === 0" class="text-center my-5 grey--text">
                <v-icon large class="mb-2">mdi-filter-remove</v-icon>
                <div>No rules match the current filters</div>
                <v-btn text color="primary" class="mt-2" @click="resetFilters">Reset filters</v-btn>
              </div>
            </div>
            
            <v-alert
              v-if="isAdmin"
              type="info"
              outlined
              class="mt-4"
            >
              As a project administrator, you cannot vote on annotation rules.
            </v-alert>
          </v-card-text>
        </v-card>
        
        <!-- Voting History -->
        <v-card 
          v-if="pastVotings.length > 0"
          outlined
          class="mt-4"
        >
          <v-card-title class="subtitle-1">
            Voting History
          </v-card-title>
          <v-card-text>
            <v-expansion-panels>
              <v-expansion-panel
                v-for="voting in pastVotings"
                :key="voting.id"
              >
                <v-expansion-panel-header>
                  <div>
                    {{ voting.description }}
                    <div class="text-caption">
                      {{ formatDate(voting.startDate) }} - {{ formatDate(voting.endDate) }}
                      <v-chip v-if="voting.endedEarly" x-small color="red" class="ml-2">Ended early</v-chip>
                    </div>
                  </div>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <div class="my-2">
                    <div class="font-weight-medium mb-2">Voting results:</div>
                    <v-list>
                      <v-list-item
                        v-for="ruleId in voting.rules"
                        :key="ruleId"
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            {{ getRuleName(ruleId) }}
                            <v-chip
                              small
                              :color="isRuleApproved(ruleId) ? 'success' : 'error'"
                              class="ml-2"
                            >
                              {{ isRuleApproved(ruleId) ? 'Approved' : 'Rejected' }}
                            </v-chip>
                          </v-list-item-title>
                          <v-list-item-subtitle>{{ getRuleDescription(ruleId) }}</v-list-item-subtitle>
                          
                          <div class="mt-2">
                            <v-chip 
                              small 
                              color="success" 
                              class="mr-2" 
                              outlined
                            >
                              <v-icon left x-small>mdi-thumb-up</v-icon>
                              Approvals: {{ ruleVotes(ruleId).aprovar }}
                            </v-chip>
                            <v-chip 
                              small 
                              color="error" 
                              outlined
                            >
                              <v-icon left x-small>mdi-thumb-down</v-icon>
                              Rejections: {{ ruleVotes(ruleId).rejeitar }}
                            </v-chip>
                          </div>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </div>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card-text>
        </v-card>
      </v-card-text>
    </v-card>
    
    <!-- Voting configuration modal -->
    <VotingConfigModal
      v-model="showVotingConfig"
      :project-id="projectId"
      @saved="handleVotingSaved"
    />
    
    <!-- Dialog to confirm ending the voting -->
    <v-dialog v-model="confirmEndVoting" max-width="500">
      <v-card>
        <v-card-title class="headline">
          Confirm ending the voting
        </v-card-title>
        <v-card-text>
          Are you sure you want to end the current voting early? This action cannot be undone.
          <v-alert type="warning" class="mt-3" dense>
            The voting will be finalized immediately and all votes will be counted in the current state.
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey darken-1" text @click="confirmEndVoting = false">
            Cancel
          </v-btn>
          <v-btn color="red darken-1" text @click="endVotingEarly">
            End Voting
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Snackbar for notifications -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
    >
      {{ snackbar.text }}
      <template #action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbar.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import { mdiPoll } from '@mdi/js'
import VotingConfigModal from '~/components/voting/VotingConfigModal.vue'

export default {
  name: 'AnnotationRulesPage',
  
  components: {
    VotingConfigModal
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      mdiPoll,
      project: {},
      showVotingConfig: false,
      confirmEndVoting: false,
      snackbar: {
        show: false,
        text: '',
        color: 'success',
        timeout: 3000
      },
      isProjectAdmin: false,
      simulateDatabaseError: false,
      filters: {
        keyword: '',
        voteStatus: null,
        voteResult: null,
        category: null,
        sortBy: 'name-asc'
      },
      voteStatusOptions: [
        { text: 'Voted', value: 'voted' },
        { text: 'Not voted', value: 'not-voted' }
      ],
      voteResultOptions: [
        { text: 'Currently approved', value: 'approved' },
        { text: 'Currently rejected', value: 'rejected' },
        { text: 'Tied', value: 'tied' }
      ],
      sortOptions: [
        { text: 'Name (A-Z)', value: 'name-asc' },
        { text: 'Name (Z-A)', value: 'name-desc' },
        { text: 'Most approvals', value: 'approvals-desc' },
        { text: 'Most rejections', value: 'rejections-desc' },
        { text: 'Recently voted', value: 'recent-votes' }
      ]
    }
  },
  
  computed: {
    isDiscussionEnded() {
      return this.$store.getters['discussion/isDiscussionEnded'](this.projectId)
    },
    ...mapGetters('voting', [
      'activeVoting', 
      'annotationRules', 
      'hasActiveVoting', 
      'ruleVotes',
      'hasUserVotedForRule',
      'getUserVoteForRule'
    ]),
    ...mapGetters('auth', ['isStaff', 'isSuperUser']),
    
    projectId() {
      return this.$route.params.id
    },
    
    isAdmin() {
      return this.isProjectAdmin || this.isStaff || this.isSuperUser
    },
    
    pastVotings() {
      return this.$store.getters['voting/pastVotings'](this.projectId)
    },
    
    filteredRules() {
      if (!this.activeVoting || !this.activeVoting.rules) {
        return []
      }
      
      // Start with all rules
      let filtered = [...this.activeVoting.rules]
      
      // Apply keyword filter
      if (this.filters.keyword) {
        const keyword = this.filters.keyword.toLowerCase()
        filtered = filtered.filter(ruleId => {
          const name = this.getRuleName(ruleId).toLowerCase()
          const description = this.getRuleDescription(ruleId).toLowerCase()
          return name.includes(keyword) || description.includes(keyword)
        })
      }
      
      // Apply vote status filter
      if (this.filters.voteStatus) {
        if (this.filters.voteStatus === 'voted') {
          filtered = filtered.filter(ruleId => this.hasVotedForRule(ruleId))
        } else if (this.filters.voteStatus === 'not-voted') {
          filtered = filtered.filter(ruleId => !this.hasVotedForRule(ruleId))
        }
      }
      
      // Apply vote result filter
      if (this.filters.voteResult) {
        filtered = filtered.filter(ruleId => {
          const votes = this.ruleVotes(ruleId)
          if (this.filters.voteResult === 'approved') {
            return votes.aprovar > votes.rejeitar
          } else if (this.filters.voteResult === 'rejected') {
            return votes.aprovar < votes.rejeitar
          } else if (this.filters.voteResult === 'tied') {
            return votes.aprovar === votes.rejeitar
          }
          return true
        })
      }
      
      // Apply category filter
      if (this.filters.category) {
        filtered = filtered.filter(ruleId => 
          this.ruleCategory(ruleId) === this.filters.category
        )
      }
      
      // Apply sorting
      if (this.filters.sortBy) {
        const sortBy = this.filters.sortBy
        
        filtered.sort((a, b) => {
          if (sortBy === 'name-asc') {
            return this.getRuleName(a).localeCompare(this.getRuleName(b))
          } else if (sortBy === 'name-desc') {
            return this.getRuleName(b).localeCompare(this.getRuleName(a))
          } else if (sortBy === 'approvals-desc') {
            return this.ruleVotes(b).aprovar - this.ruleVotes(a).aprovar
          } else if (sortBy === 'rejections-desc') {
            return this.ruleVotes(b).rejeitar - this.ruleVotes(a).rejeitar
          } else if (sortBy === 'recent-votes') {
            // This would require vote timestamps, which we might not have
            // Fallback to name sorting
            return this.getRuleName(a).localeCompare(this.getRuleName(b))
          }
          
          return 0
        })
      }
      
      return filtered
    },
    
    getCategoryOptions() {
      if (!this.activeVoting || !this.activeVoting.rules) {
        return []
      }
      
      // Get unique categories from all rules
      const categories = new Set()
      
      this.activeVoting.rules.forEach(ruleId => {
        const category = this.ruleCategory(ruleId)
        if (category) {
          categories.add(category)
        }
      })
      
      return Array.from(categories).map(category => ({
        text: category,
        value: category
      }))
    }
  },

  async mounted() {
    const projectId = this.$route.params.id
    this.project = await this.$services.project.findById(projectId)
    
    // Reset simulation error state
    this.simulateDatabaseError = false
    
    // Load discussion state
    this.$store.dispatch('discussion/initDiscussionState')
    
    // Load voting state
    this.$store.dispatch('voting/initVotingState', projectId)
    
    // Check if user is project administrator
    this.checkAdminRole()
  },
  
  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR')
    },
    
    getRuleName(ruleId) {
      const rule = this.annotationRules.find(r => r.id === ruleId)
      return rule ? rule.name : 'Rule not found'
    },
    
    getRuleDescription(ruleId) {
      const rule = this.annotationRules.find(r => r.id === ruleId)
      return rule ? rule.description : ''
    },
    
    ruleCategory(ruleId) {
      const rule = this.annotationRules.find(r => r.id === ruleId)
      return rule && rule.category ? rule.category : null
    },
    
    voteForRule(ruleId, vote) {
      // Check if user is admin
      if (this.isAdmin) {
        this.snackbar = {
          show: true,
          text: 'Administrators cannot vote on annotation rules',
          color: 'error',
          timeout: 3000
        }
        return
      }
      
      // Simulate database error if flag is active
      if (this.simulateDatabaseError) {
        this.snackbar = {
          show: true,
          text: 'Error: Database unavailable. Try again later.',
          color: 'error',
          timeout: 5000
        }
        return
      }
      
      // Call action to register vote in store
      this.$store.dispatch('voting/voteForRule', { ruleId, vote })
      
      this.snackbar = {
        show: true,
        text: `You ${vote === 'aprovar' ? 'approved' : 'rejected'} the rule: ${this.getRuleName(ruleId)}`,
        color: vote === 'aprovar' ? 'success' : 'error',
        timeout: 3000
      }
    },
    
    hasVotedForRule(ruleId) {
      // Use store getter to check if user has already voted
      return this.hasUserVotedForRule(ruleId)
    },
    
    handleVotingSaved(votingData) {
      // Display success notification
      this.snackbar = {
        show: true,
        text: 'Voting configured successfully!',
        color: 'success',
        timeout: 3000
      }
      
      // Ensure voting state is updated
      this.$store.commit('voting/SET_ACTIVE_VOTING', {
        projectId: this.projectId,
        voting: votingData
      })
    },
    
    async checkAdminRole() {
      try {
        const member = await this.$repositories.member.fetchMyRole(this.projectId)
        this.isProjectAdmin = member.isProjectAdmin
      } catch (error) {
        console.error('Error checking administrator role:', error)
      }
    },
    
    async endVotingEarly() {
      try {
        // Call action to end voting early
        const result = await this.$store.dispatch('voting/endVotingEarly', {
          projectId: this.projectId
        })
        
        if (result.success) {
          this.snackbar = {
            show: true,
            text: 'Voting ended successfully!',
            color: 'success',
            timeout: 3000
          }
          this.confirmEndVoting = false
        } else {
          throw new Error('Error ending voting')
        }
      } catch (error) {
        console.error('Error ending voting:', error)
        this.snackbar = {
          show: true,
          text: 'An error occurred while ending the voting',
          color: 'error',
          timeout: 3000
        }
      }
    },
    
    isRuleApproved(ruleId) {
      const votes = this.ruleVotes(ruleId)
      return votes.aprovar > votes.rejeitar
    },
    
    resetFilters() {
      this.filters = {
        keyword: '',
        voteStatus: null,
        voteResult: null,
        category: null,
        sortBy: 'name-asc'
      }
    }
  }
}
</script> 