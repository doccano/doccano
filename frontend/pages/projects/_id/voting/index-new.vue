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
            <h2>Votação</h2>
          </v-card-title>

          <v-card-text>
            <!-- Interface para Administradores -->
            <div v-if="isProjectAdmin">
              <!-- Header with Create Button -->
              <div class="d-flex justify-space-between align-center mb-6">
                <div>
                  <p class="text-body-2 grey--text mb-0">
                    Gerenciar configurações de votação
                  </p>
                </div>
                <v-btn
                  :color="canConfigureVoting ? 'primary' : 'grey'"
                  :disabled="!canConfigureVoting"
                  @click="goToConfiguration"
                >
                  <v-icon left>{{ mdiPlus }}</v-icon>
                  Criar Nova Votação
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
                            {{ formatDate(config.start_date) }} - {{ formatDate(config.end_date) }} | 
                            {{ config.annotation_rules.length }} regras
                          </div>
                        </div>
                        <v-spacer />
                        <v-chip
                          :color="getVotingStatusColor(config)"
                          dark
                          small
                          class="mr-2"
                        >
                          {{ getVotingStatusText(config) }}
                        </v-chip>
                        <v-chip
                          :color="getVotingMethodColor(config.voting_method)"
                          dark
                          small
                          class="mr-2"
                        >
                          {{ getVotingMethodText(config.voting_method) }}
                        </v-chip>
                      </div>
                    </v-expansion-panel-header>

                    <v-expansion-panel-content>
                      <v-card flat>
                        <v-card-text class="pa-0 pt-4">
                          <v-row>
                            <!-- Basic Information -->
                            <v-col cols="12" md="6">
                              <h4 class="text-h6 mb-3">Informações Básicas</h4>
                              <div class="mb-2">
                                <strong>Descrição:</strong> {{ config.description }}
                              </div>
                              <div class="mb-2">
                                <strong>Período:</strong> {{ formatDate(config.start_date) }} - {{ formatDate(config.end_date) }}
                              </div>
                              <div class="mb-2">
                                <strong>Horário:</strong> {{ config.start_time }} - {{ config.end_time }}
                              </div>
                              <div class="mb-2">
                                <strong>Criado em:</strong> {{ formatDateTime(config.created_at) }}
                              </div>
                            </v-col>

                            <!-- Voting Method -->
                            <v-col cols="12" md="6">
                              <h4 class="text-h6 mb-3">Método de Votação</h4>
                              <v-chip
                                :color="getVotingMethodColor(config.voting_method)"
                                dark
                                class="mb-2"
                              >
                                {{ getVotingMethodText(config.voting_method) }}
                              </v-chip>
                              <p class="text-body-2 grey--text mt-2">
                                {{ getVotingMethodDescription(config.voting_method) }}
                              </p>
                            </v-col>

                            <!-- Annotation Rules -->
                            <v-col cols="12">
                              <h4 class="text-h6 mb-3">Regras de Anotação ({{ config.annotation_rules.length }})</h4>
                              <v-row>
                                <v-col
                                  v-for="(rule) in config.annotation_rules"
                                  :key="rule.id"
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

                            <!-- Voting Results (for admins) -->
                            <v-col v-if="votingResults[config.id]" cols="12">
                              <v-divider class="my-4" />
                              <h4 class="text-h6 mb-3">Resultados da Votação</h4>
                              <v-card outlined>
                                <v-card-text>
                                  <div v-for="result in votingResults[config.id]" :key="result.rule_id" class="mb-4">
                                    <div class="font-weight-bold mb-2">{{ result.rule_name }}</div>
                                    <div class="mb-2">
                                      <v-chip 
                                        color="success" 
                                        small 
                                        class="mr-2"
                                      >
                                        <v-icon left small>mdi-thumb-up</v-icon>
                                        Aprovações: {{ result.approve_votes }}
                                      </v-chip>
                                      <v-chip 
                                        color="error" 
                                        small 
                                        class="mr-2"
                                      >
                                        <v-icon left small>mdi-thumb-down</v-icon>
                                        Reprovações: {{ result.disapprove_votes }}
                                      </v-chip>
                                      <v-chip 
                                        color="grey" 
                                        small
                                      >
                                        <v-icon left small>mdi-minus</v-icon>
                                        Neutros: {{ result.neutral_votes }}
                                      </v-chip>
                                    </div>
                                    <v-progress-linear
                                      :value="result.approval_percentage"
                                      height="8"
                                      color="success"
                                      background-color="error"
                                      class="mb-1"
                                    />
                                    <div class="text-caption grey--text">
                                      {{ result.approval_percentage }}% de aprovação
                                    </div>
                                  </div>
                                  
                                  <v-divider class="my-3" />
                                  <div class="text-center">
                                    <strong>Total de Participantes: {{ getTotalParticipants(config.id) }}</strong>
                                  </div>
                                </v-card-text>
                              </v-card>
                            </v-col>
                          </v-row>

                          <!-- Actions -->
                          <v-divider class="my-4" />
                          <div class="d-flex justify-end">
                            <v-btn
                              text
                              color="primary"
                              class="mr-2"
                              @click="editConfiguration(config)"
                            >
                              <v-icon left>{{ mdiPencil }}</v-icon>
                              Editar
                            </v-btn>
                            <v-btn
                              text
                              color="error"
                              @click="deleteConfiguration(config, index)"
                            >
                              <v-icon left>{{ mdiDelete }}</v-icon>
                              Excluir
                            </v-btn>
                          </div>
                        </v-card-text>
                      </v-card>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>

              <!-- No configurations message -->
              <div v-else-if="!canConfigureVoting" class="text-center py-8">
                <v-alert
                  color="warning"
                  outlined
                  :icon="false"
                >
                  <strong>Aguardando o fim das discussões!</strong><br>
                  Para criar votações, é necessário que todas as discussões estejam fechadas.
                  <br><br>
                  <v-btn
                    color="primary"
                    small
                    @click="goToDiscussions"
                  >
                    <v-icon left small>{{ mdiComment }}</v-icon>
                    Ver Discussões
                  </v-btn>
                </v-alert>
              </div>

              <div v-else class="text-center py-8">
                <v-alert
                  color="success"
                  outlined
                  :icon="false"
                >
                  <strong>Pronto para criar votações!</strong><br>
                  Todas as discussões estão fechadas. Você pode criar uma nova configuração de votação.
                </v-alert>
              </div>
            </div>

            <!-- Interface para Usuários -->
            <div v-else>
              <div class="mb-6">
                <h3 class="text-h5 mb-2">Votações Disponíveis</h3>
                <p class="text-body-2 grey--text">
                  Vote nas regras de anotação para contribuir com o projeto.
                </p>
              </div>

              <!-- Active Voting for Users -->
              <div v-if="activeVotingForUsers.length > 0">
                <v-card
                  v-for="config in activeVotingForUsers"
                  :key="config.id"
                  class="mb-4"
                  outlined
                >
                  <v-card-title>
                    <v-icon class="mr-3" color="primary">{{ mdiVote }}</v-icon>
                    {{ config.name }}
                    <v-spacer />
                    <v-chip color="success" dark small>
                      <v-icon left small>mdi-clock</v-icon>
                      Ativa
                    </v-chip>
                  </v-card-title>
                  
                  <v-card-subtitle>
                    {{ config.description }}
                  </v-card-subtitle>

                  <v-card-text>
                    <div class="mb-4">
                      <v-chip
                        :color="getVotingMethodColor(config.voting_method)"
                        dark
                        small
                        class="mb-2"
                      >
                        {{ getVotingMethodText(config.voting_method) }}
                      </v-chip>
                      <p class="text-body-2 grey--text mt-2">
                        {{ getVotingMethodDescription(config.voting_method) }}
                      </p>
                    </div>

                    <div class="mb-4">
                      <strong>Período:</strong> {{ formatDate(config.start_date) }} - {{ formatDate(config.end_date) }}<br>
                      <strong>Horário:</strong> {{ config.start_time }} - {{ config.end_time }}
                    </div>

                    <v-divider class="my-4" />

                    <h4 class="text-h6 mb-4">Regras de Anotação</h4>
                    
                    <div v-for="rule in config.annotation_rules" :key="rule.id" class="mb-6">
                      <v-card outlined class="mb-3">
                        <v-card-text>
                          <h5 class="text-subtitle-1 font-weight-bold mb-2">
                            {{ rule.name }}
                          </h5>
                          <p class="text-body-2 mb-3">
                            {{ rule.description }}
                          </p>
                          
                          <!-- Voting Controls -->
                          <div class="d-flex align-center">
                            <span class="text-body-2 mr-4 font-weight-medium">Seu voto:</span>
                            
                            <!-- Current status indicator -->
                            <v-chip
                              v-if="!getUserVote(config.id, rule.id)"
                              color="grey lighten-1"
                              small
                              outlined
                              class="mr-3"
                            >
                              <v-icon left small>mdi-help-circle-outline</v-icon>
                              Não votado
                            </v-chip>
                            
                            <!-- Vote status chip when voted -->
                            <v-chip
                              v-else
                              :color="getUserVote(config.id, rule.id) === 'approve' ? 'success' : 'error'"
                              small
                              dark
                              class="mr-3"
                            >
                              <v-icon left small>
                                {{ getUserVote(config.id, rule.id) === 'approve' ? 'mdi-check-circle' : 'mdi-close-circle' }}
                              </v-icon>
                              {{ getUserVote(config.id, rule.id) === 'approve' ? 'Aprovado' : 'Reprovado' }}
                            </v-chip>
                            
                            <!-- Voting buttons based on method -->
                            <!-- Approve/Disapprove Toggle -->
                            <div v-if="config.voting_method === 'approve_disapprove'" class="d-flex">
                              <v-btn
                                :color="getUserVote(config.id, rule.id) === 'approve' ? 'success' : 'grey lighten-1'"
                                :dark="getUserVote(config.id, rule.id) === 'approve'"
                                :outlined="getUserVote(config.id, rule.id) !== 'approve'"
                                small
                                class="mr-2 vote-button"
                                @click="vote(config.id, rule.id, getUserVote(config.id, rule.id) === 'approve' ? null : 'approve')"
                              >
                                <v-icon small class="mr-1">
                                  {{ getUserVote(config.id, rule.id) === 'approve' ? 'mdi-check-circle' : 'mdi-thumb-up' }}
                                </v-icon>
                                {{ getUserVote(config.id, rule.id) === 'approve' ? 'APROVADO ✓' : 'APROVAR' }}
                              </v-btn>
                              
                              <v-btn
                                :color="getUserVote(config.id, rule.id) === 'disapprove' ? 'error' : 'grey lighten-1'"
                                :dark="getUserVote(config.id, rule.id) === 'disapprove'"
                                :outlined="getUserVote(config.id, rule.id) !== 'disapprove'"
                                small
                                class="vote-button"
                                @click="vote(config.id, rule.id, getUserVote(config.id, rule.id) === 'disapprove' ? null : 'disapprove')"
                              >
                                <v-icon small class="mr-1">
                                  {{ getUserVote(config.id, rule.id) === 'disapprove' ? 'mdi-close-circle' : 'mdi-thumb-down' }}
                                </v-icon>
                                {{ getUserVote(config.id, rule.id) === 'disapprove' ? 'REPROVADO ✗' : 'REPROVAR' }}
                              </v-btn>
                            </div>

                            <!-- Approve Only -->
                            <div v-else-if="config.voting_method === 'approve_only'">
                              <v-btn
                                :color="getUserVote(config.id, rule.id) === 'approve' ? 'success' : 'grey lighten-1'"
                                :dark="getUserVote(config.id, rule.id) === 'approve'"
                                :outlined="getUserVote(config.id, rule.id) !== 'approve'"
                                small
                                class="vote-button"
                                @click="vote(config.id, rule.id, getUserVote(config.id, rule.id) === 'approve' ? null : 'approve')"
                              >
                                <v-icon small class="mr-1">
                                  {{ getUserVote(config.id, rule.id) === 'approve' ? 'mdi-check-circle' : 'mdi-thumb-up' }}
                                </v-icon>
                                {{ getUserVote(config.id, rule.id) === 'approve' ? 'APROVADO ✓' : 'APROVAR' }}
                              </v-btn>
                            </div>

                            <!-- Disapprove Only -->
                            <div v-else-if="config.voting_method === 'disapprove_only'">
                              <v-btn
                                :color="getUserVote(config.id, rule.id) === 'disapprove' ? 'error' : 'grey lighten-1'"
                                :dark="getUserVote(config.id, rule.id) === 'disapprove'"
                                :outlined="getUserVote(config.id, rule.id) !== 'disapprove'"
                                small
                                class="vote-button"
                                @click="vote(config.id, rule.id, getUserVote(config.id, rule.id) === 'disapprove' ? null : 'disapprove')"
                              >
                                <v-icon small class="mr-1">
                                  {{ getUserVote(config.id, rule.id) === 'disapprove' ? 'mdi-close-circle' : 'mdi-thumb-down' }}
                                </v-icon>
                                {{ getUserVote(config.id, rule.id) === 'disapprove' ? 'REPROVADO ✗' : 'REPROVAR' }}
                              </v-btn>
                            </div>
                          </div>
                          
                          <!-- Vote status indicator -->
                          <div class="mt-3">
                            <!-- When user has voted -->
                            <v-alert
                              v-if="getUserVote(config.id, rule.id)"
                              :type="getUserVote(config.id, rule.id) === 'approve' ? 'success' : 'error'"
                              dense
                              text
                              class="mb-0"
                            >
                              <div class="d-flex align-center">
                                <v-icon small class="mr-2">
                                  {{ getUserVote(config.id, rule.id) === 'approve' ? 'mdi-check-circle' : 'mdi-close-circle' }}
                                </v-icon>
                                <span class="text-body-2">
                                  Você {{ getUserVote(config.id, rule.id) === 'approve' ? 'aprovou' : 'reprovou' }} esta regra
                                </span>
                              </div>
                            </v-alert>
                            
                            <!-- When user hasn't voted -->
                            <v-alert
                              v-else
                              type="info"
                              dense
                              text
                              class="mb-0"
                            >
                              <div class="d-flex align-center">
                                <v-icon small class="mr-2">mdi-information</v-icon>
                                <span class="text-body-2">Aguardando seu voto nesta regra</span>
                              </div>
                            </v-alert>
                          </div>
                        </v-card-text>
                      </v-card>
                    </div>
                  </v-card-text>
                </v-card>
              </div>

              <!-- No active voting message -->
              <div v-else class="text-center py-8">
                <v-alert
                  color="info"
                  outlined
                  :icon="false"
                >
                  <strong>Nenhuma votação ativa no momento</strong><br>
                  Aguarde novas votações serem criadas pelos administradores do projeto.
                </v-alert>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading overlay -->
    <v-overlay :value="isLoading">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
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
  mdiAlert,
  mdiComment
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
      mdiComment,
      discussions: [],
      votingConfigurations: [],
      votingResults: {},
      userVotes: {},
      isLoading: false
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      await this.$services.project.findById(this.$route.params.id)
      
      // Carregar informações do membro atual
      await this.$store.dispatch('projects/setCurrentMember', {
        projectId: this.$route.params.id,
        $repositories: this.$repositories
      })
      
      // Fetch discussions to check their status
      const discussionsRes = await this.$axios.get(`/v1/projects/${this.$route.params.id}/discussions/`)
      this.discussions = Array.isArray(discussionsRes.data?.results) ? discussionsRes.data.results : []
      
      // Load voting configurations from API
      await this.loadVotingConfigurations()
      
      // Load user votes for active configurations
      await this.loadUserVotes()
      
      // Load voting results for admin
      if (this.isProjectAdmin) {
        await this.loadVotingResults()
      }
    } catch(e) {
      throw new Error(e.response?.data?.detail || e.message)
    } finally {
      this.isLoading = false
    }
  },

  head() {
    return {
      title: 'Voting'
    }
  },

  computed: {
    project() {
      return this.$store.getters['projects/project']
    },
    
    isProjectAdmin() {
      return this.$store.getters['projects/isProjectAdmin']
    },

    currentUserId() {
      return this.$store.getters['auth/getUserId']
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
    },

    activeVotingForUsers() {
      const now = new Date()
      const currentDate = now.toISOString().substr(0, 10)
      const currentTime = now.toTimeString().substr(0, 5)

      return this.votingConfigurations.filter(config => {
        const startDate = config.start_date
        const endDate = config.end_date
        const startTime = config.start_time
        const endTime = config.end_time

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
    }
  },

  methods: {
    async loadVotingConfigurations() {
      try {
        this.votingConfigurations = await this.$services.voting.list(this.$route.params.id)
      } catch (error) {
        console.error('Error loading voting configurations:', error)
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Erro ao carregar configurações de votação',
          timeout: 4000
        })
      }
    },

    async loadUserVotes() {
      try {
        const userVotesObj = {}
        for (const config of this.votingConfigurations) {
          const votes = await this.$services.voting.getUserVotes(this.$route.params.id, config.id.toString())
          votes.forEach(vote => {
            const key = `${vote.configuration_id}_${vote.rule_id}`
            userVotesObj[key] = vote.vote
          })
        }
        this.userVotes = userVotesObj
      } catch (error) {
        console.error('Error loading user votes:', error)
      }
    },

    async loadVotingResults() {
      try {
        const resultsObj = {}
        for (const config of this.votingConfigurations) {
          const results = await this.$services.voting.getResults(this.$route.params.id, config.id.toString())
          resultsObj[config.id] = results
        }
        this.votingResults = resultsObj
      } catch (error) {
        console.error('Error loading voting results:', error)
      }
    },

    goToConfiguration() {
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting/configure`))
    },

    editConfiguration(config) {
      // Store the configuration ID to edit in session storage
      sessionStorage.setItem('editingConfigId', config.id.toString())
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting/configure`))
    },

    async deleteConfiguration(config) {
      const confirmed = await this.$confirm(`Tem certeza de que deseja excluir a configuração de votação "${config.name}"?`, {
        title: 'Excluir Configuração',
        buttonTrueText: 'Excluir',
        buttonFalseText: 'Cancelar',
        color: 'error'
      })

      if (confirmed) {
        try {
          await this.$services.voting.delete(this.$route.params.id, config.id.toString())
          await this.loadVotingConfigurations()
          this.$store.dispatch('notification/setNotification', {
            color: 'success',
            text: 'Configuração excluída com sucesso',
            timeout: 4000
          })
        } catch (error) {
          console.error('Error deleting configuration:', error)
          this.$store.dispatch('notification/setNotification', {
            color: 'error',
            text: 'Erro ao excluir configuração',
            timeout: 4000
          })
        }
      }
    },

    goToDiscussions() {
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/discussions`))
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },

    formatDateTime(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('pt-BR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getVotingMethodText(method) {
      const methods = {
        'approve_only': 'Apenas Aprovar',
        'disapprove_only': 'Apenas Reprovar',
        'approve_disapprove': 'Aprovar ou Reprovar'
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
        'approve_only': 'Anotadores podem apenas aprovar regras que apoiam',
        'disapprove_only': 'Anotadores podem apenas reprovar regras que se opõem',
        'approve_disapprove': 'Anotadores podem aprovar ou reprovar cada regra'
      }
      return descriptions[method] || ''
    },

    getVotingStatusText(config) {
      const now = new Date()
      const currentDate = now.toISOString().substr(0, 10)
      const currentTime = now.toTimeString().substr(0, 5)
      
      if (currentDate < config.start_date || (currentDate === config.start_date && currentTime < config.start_time)) {
        return 'Aguardando Início'
      } else if (currentDate > config.end_date || (currentDate === config.end_date && currentTime >= config.end_time)) {
        return 'Encerrada'
      } else {
        return 'Em Andamento'
      }
    },

    getVotingStatusColor(config) {
      const now = new Date()
      const currentDate = now.toISOString().substr(0, 10)
      const currentTime = now.toTimeString().substr(0, 5)
      
      if (currentDate < config.start_date || (currentDate === config.start_date && currentTime < config.start_time)) {
        return 'warning'
      } else if (currentDate > config.end_date || (currentDate === config.end_date && currentTime >= config.end_time)) {
        return 'grey'
      } else {
        return 'success'
      }
    },

    getUserVote(configId, ruleId) {
      const key = `${configId}_${ruleId}`
      return this.userVotes[key] || null
    },

    async vote(configId, ruleId, vote) {
      try {
        const voteData = {
          rule_id: ruleId,
          vote
        }

        if (vote === null) {
          // Remove vote
          await this.$services.voting.removeVote(this.$route.params.id, configId.toString(), ruleId.toString())
        } else {
          // Submit vote
          await this.$services.voting.submitVote(this.$route.params.id, configId.toString(), voteData)
        }

        // Update local state
        const key = `${configId}_${ruleId}`
        if (vote === null) {
          this.$delete(this.userVotes, key)
        } else {
          this.$set(this.userVotes, key, vote)
        }

        // Show confirmation
        let message = ''
        let color = 'success'
        
        if (vote === null) {
          message = 'Voto removido com sucesso!'
          color = 'info'
        } else {
          message = `Voto registrado: ${vote === 'approve' ? 'APROVADO ✓' : 'REPROVADO ✗'}`
          color = vote === 'approve' ? 'success' : 'error'
        }
        
        this.$store.dispatch('notification/setNotification', {
          color,
          text: message,
          timeout: 4000
        })

        // Reload results if admin
        if (this.isProjectAdmin) {
          await this.loadVotingResults()
        }

      } catch (error) {
        console.error('Error voting:', error)
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Erro ao registrar voto',
          timeout: 4000
        })
      }
    },

    getTotalParticipants(configId) {
      const results = this.votingResults[configId]
      if (!results || results.length === 0) {
        return 0
      }

      // Get unique participant count from the results
      const allUsers = new Set()
      results.forEach(result => {
        // This is a simplified calculation - in a real implementation,
        // you might want to track unique participants differently
        allUsers.add(result.total_votes)
      })
      
      return Math.max(...results.map(r => r.total_votes))
    }
  }
}
</script>

<style scoped>
/* Transições suaves para os botões de votação */
.v-btn {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

/* Efeito hover melhorado */
.v-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
}

/* Animação para alertas de status */
.v-alert {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Destaque para botões de votação */
.vote-button {
  min-width: 120px !important;
}

/* Status chips styling */
.v-chip {
  font-weight: 500;
}
</style>
