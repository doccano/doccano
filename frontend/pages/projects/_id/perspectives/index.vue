<template>
  <v-container fluid>
    <!-- Database Error Alert - Always visible when database is down -->
    <v-alert
      v-if="!isDatabaseHealthy"
      type="error"
      prominent
      class="mb-4"
      ref="databaseAlert"
    >
      <v-row align="center">
        <v-col class="grow">
          <div class="title">De momento a base de dados não se encontra disponível. Por favor, tente mais tarde.</div>
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
            <h2>{{ $t('perspectives.perspectives') }}</h2>
            <v-spacer />
            
            <!-- Clear Filters Button (Admin Only) -->
            <v-btn
              v-if="hasActiveFilters && isProjectAdmin"
              color="red"
              class="mr-3"
              @click="clearFilters"
            >
              <v-icon left>mdi-filter-remove</v-icon>
              Clear Filters
            </v-btn>
            
            <!-- Add Question Button -->
            <v-btn
              v-if="isProjectAdmin"
              color="primary"
              @click="showCreateDialog = true"
            >
              <v-icon left>{{ mdiPlus }}</v-icon>
              {{ $t('perspectives.addQuestion') }}
            </v-btn>
          </v-card-title>

          <!-- Filters and Search Section (Admin Only) -->
          <v-card-text v-if="isProjectAdmin" class="pb-0">
            <v-expansion-panels v-model="filtersExpanded" flat>
              <v-expansion-panel>
                <v-expansion-panel-header class="pa-0">
                  <div class="d-flex align-center">
                    <v-icon class="mr-2">mdi-filter-variant</v-icon>
                    <span class="font-weight-medium">Filters & Search</span>
                    <v-spacer />
                    <v-chip
                      v-if="hasActiveFilters"
                      color="primary"
                      text-color="white"
                      small
                      class="mr-2"
                    >
                      {{ activeFiltersCount }} active
                    </v-chip>
                  </div>
                </v-expansion-panel-header>
                
                <v-expansion-panel-content class="pt-4">
                  <v-row>
                    <!-- Search Bar -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="searchQuery"
                        label="Search items..."
                        prepend-inner-icon="mdi-magnify"
                        outlined
                        dense
                        clearable
                        hide-details
                        @input="applyFilters"
                      />
                    </v-col>

                    <!-- Answer Filter -->
                    <v-col cols="12" md="3">
                      <v-select
                        v-model="filters.answerFilter"
                        :items="answerFilterOptions"
                        label="Filter by Answer"
                        prepend-inner-icon="mdi-comment-search"
                        outlined
                        dense
                        clearable
                        hide-details
                        @change="applyFilters"
                      />
                    </v-col>

                    <!-- Item Type Filter -->
                    <v-col cols="12" md="3">
                      <v-select
                        v-model="filters.questionType"
                        :items="questionTypeOptions"
                        label="Item Type"
                        outlined
                        dense
                        clearable
                        hide-details
                        @change="applyFilters"
                      />
                    </v-col>

                    <!-- Data Type Filter -->
                    <v-col cols="12" md="3">
                      <v-select
                        v-model="filters.dataType"
                        :items="dataTypeOptions"
                        label="Data Type"
                        outlined
                        dense
                        clearable
                        hide-details
                        @change="applyFilters"
                      />
                    </v-col>

                    <!-- Required Filter -->
                    <v-col cols="12" md="3">
                      <v-select
                        v-model="filters.isRequired"
                        :items="requiredOptions"
                        label="Required"
                        outlined
                        dense
                        clearable
                        hide-details
                        @change="applyFilters"
                      />
                    </v-col>

                    <!-- Answer Count Filter -->
                    <v-col cols="12" md="3">
                      <v-select
                        v-model="filters.answerCount"
                        :items="answerCountOptions"
                        label="Answer Count"
                        outlined
                        dense
                        clearable
                        hide-details
                        @change="applyFilters"
                      />
                    </v-col>

                    <!-- Sort By -->
                    <v-col cols="12" md="3">
                      <v-select
                        v-model="sortBy"
                        :items="sortOptions"
                        label="Sort By"
                        outlined
                        dense
                        hide-details
                        @change="applyFilters"
                      />
                    </v-col>

                    <!-- Sort Order -->
                    <v-col cols="12" md="3">
                      <v-select
                        v-model="sortOrder"
                        :items="sortOrderOptions"
                        label="Sort Order"
                        outlined
                        dense
                        hide-details
                        @change="applyFilters"
                      />
                    </v-col>
                  </v-row>

                  <!-- Clear Filters Button -->
                  <v-row class="mt-2">
                    <v-col cols="12" class="text-right">
                      <v-btn
                        v-if="hasActiveFilters"
                        color="grey"
                        text
                        small
                        @click="clearFilters"
                      >
                        <v-icon left small>mdi-filter-remove</v-icon>
                        Clear All Filters
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card-text>

          <v-tabs v-model="activeTab" background-color="transparent" :disabled="!isDatabaseHealthy">
            <v-tab key="questions">Items</v-tab>
            <v-tab v-if="isProjectAdmin" key="statistics">{{ $t('perspectives.statistics') }}</v-tab>
          </v-tabs>

          <v-tabs-items v-model="activeTab">
            <!-- Items Tab -->
            <v-tab-item key="questions">
              <v-card-text>
                                  <div v-if="isProjectAdmin">
                  <h3 class="mb-4">Manage Items</h3>
                  
                  <!-- Results Summary -->
                  <v-alert
                    v-if="hasActiveFilters && filteredQuestions.length !== questions.length"
                    type="info"
                    outlined
                    dense
                    class="mb-4"
                  >
                    <v-icon left>mdi-information</v-icon>
                    Showing {{ filteredQuestions.length }} of {{ questions.length }} items
                  </v-alert>
                  
                  <question-list
                    :questions="filteredQuestions"
                    :loading="loading"
                    @edit="editQuestion"
                    @delete="deleteQuestion"
                  />
                </div>
                                  <div v-else>
                  <h3 class="mb-4">Answer Items</h3>
                  
                  <question-answer-form
                    :questions="questions"
                    :loading="loading"
                    @answer="submitAnswer"
                    @cancel-answer="cancelAnswer"
                  />
                </div>
              </v-card-text>
            </v-tab-item>

            <!-- Statistics Tab (Admin only) -->
            <v-tab-item v-if="isProjectAdmin" key="statistics">
              <v-card-text>
                <h3 class="mb-4">{{ $t('perspectives.projectStatistics') }}</h3>
                <perspective-stats
                  :stats="projectStats"
                  :loading="statsLoading"
                />
              </v-card-text>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Question Dialog -->
    <v-dialog v-model="showCreateDialog" max-width="600px">
      <question-form
        :question="editingQuestion"
        :loading="formLoading"
        :next-order="nextOrder"
        @save="saveQuestion"
        @cancel="closeDialog"
      />
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="400px">
      <v-card>
        <v-card-title>{{ $t('perspectives.confirmDelete') }}</v-card-title>
        <v-card-text>
          {{ $t('perspectives.deleteQuestionConfirm') }}
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showDeleteDialog = false">{{ $t('generic.cancel') }}</v-btn>
          <v-btn color="error" @click="confirmDelete">{{ $t('generic.delete') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Database Connection Error Dialog -->
    <v-dialog v-model="showDatabaseErrorDialog" max-width="450px" persistent>
      <v-card>
        <v-card-title class="headline error--text">
          <v-icon color="error" class="mr-2">mdi-database-alert</v-icon>
          {{ $t('perspectives.databaseConnectionErrorTitle') }}
        </v-card-title>
        <v-card-text class="pt-4">
          <v-alert type="error" outlined class="mb-3">
            {{ $t('perspectives.databaseConnectionError') }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" @click="showDatabaseErrorDialog = false">
            {{ $t('generic.ok') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import { mdiPlus } from '@mdi/js'
import QuestionList from '@/components/perspective/QuestionList.vue'
import QuestionAnswerForm from '@/components/perspective/QuestionAnswerForm.vue'
import QuestionForm from '@/components/perspective/QuestionForm.vue'
import PerspectiveStats from '@/components/perspective/PerspectiveStats.vue'
import { databaseHealthMixin } from '@/mixins/databaseHealthMixin'

export default {
  components: {
    QuestionList,
    QuestionAnswerForm,
    QuestionForm,
    PerspectiveStats
  },

  mixins: [databaseHealthMixin],

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      mdiPlus,
      activeTab: 0,
      questions: [],
      filteredQuestions: [],
      projectStats: null,
      loading: false,
      statsLoading: false,
      formLoading: false,
      showCreateDialog: false,
      showDeleteDialog: false,
      showDatabaseErrorDialog: false,
      editingQuestion: null,
      questionToDelete: null,
      isProjectAdmin: false,
      currentMember: null,
      
      // Filters and Search
      filtersExpanded: 0,
      searchQuery: '',
      filters: {
        questionType: null,
        dataType: null,
        isRequired: null,
        answerCount: null,
        answerFilter: null
      },
      sortBy: 'order',
      sortOrder: 'asc',
      
      // Filter Options
      questionTypeOptions: [
        { text: 'Open Text', value: 'open' },
        { text: 'Multiple Choice', value: 'closed' }
      ],
      dataTypeOptions: [
        { text: 'String', value: 'string' },
        { text: 'Integer', value: 'integer' }
      ],
      requiredOptions: [
        { text: 'Required', value: true },
        { text: 'Optional', value: false }
      ],
      answerCountOptions: [
        { text: 'No answers (0)', value: 'none' },
        { text: 'Few answers (1-5)', value: 'few' },
        { text: 'Many answers (6+)', value: 'many' }
      ],
      sortOptions: [
        { text: 'Order', value: 'order' },
        { text: 'Item Text', value: 'text' },
        { text: 'Item Type', value: 'questionType' },
        { text: 'Data Type', value: 'dataType' },
        { text: 'Answer Count', value: 'answerCount' },
        { text: 'Created Date', value: 'createdAt' }
      ],
      sortOrderOptions: [
        { text: 'Ascending', value: 'asc' },
        { text: 'Descending', value: 'desc' }
      ],
      answerFilterOptions: []
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    ...mapGetters('auth', ['getUserId']),

    projectId() {
      return this.$route.params.id
    },

    nextOrder() {
      if (this.questions.length === 0) {
        return 1
      }
      const maxOrder = Math.max(...this.questions.map(q => q.order))
      return maxOrder + 1
    },

    hasActiveFilters() {
      return !!(
        this.searchQuery ||
        this.filters.questionType ||
        this.filters.dataType ||
        this.filters.isRequired !== null ||
        this.filters.answerCount ||
        this.filters.answerFilter
      )
    },

    activeFiltersCount() {
      let count = 0
      if (this.searchQuery) count++
      if (this.filters.questionType) count++
      if (this.filters.dataType) count++
      if (this.filters.isRequired !== null) count++
      if (this.filters.answerCount) count++
      if (this.filters.answerFilter) count++
      return count
    }
  },

  async mounted() {
    await this.loadAdminStatus()
    if (this.currentMember) {
      await this.loadQuestions()
      if (this.isProjectAdmin) {
        await this.loadStats()
      }
    } else {
      this.$store.dispatch('notification/setNotification', {
        color: 'error',
        text: 'Unable to load member information'
      })
    }
  },

  watch: {
    isDatabaseHealthy(newValue, oldValue) {
      // When database becomes unhealthy, scroll to show the error message
      if (oldValue === true && newValue === false) {
        this.$nextTick(() => {
          if (this.$refs.databaseAlert) {
            this.$refs.databaseAlert.$el.scrollIntoView({ 
              behavior: 'smooth', 
              block: 'center' 
            })
          }
        })
      }
    }
  },

  methods: {
    async loadAdminStatus() {
      try {
        this.currentMember = await this.$repositories.member.fetchMyRole(this.projectId)
        this.isProjectAdmin = this.currentMember.isProjectAdmin
      } catch (error) {
        console.error('Failed to load admin status:', error)
      }
    },

    async loadQuestions() {
      if (!this.currentMember || !this.currentMember.id) {
        console.error('No current member available')
        return
      }

      console.log('Loading questions for project:', this.projectId, 'member:', this.currentMember.id, 'isAdmin:', this.isProjectAdmin)

      this.loading = true
      try {
        if (this.isProjectAdmin) {
          // Admin sees all questions - but still needs to provide a member_id for the API
          // We'll use the admin's own member_id
          console.log('Loading questions as admin')
          const params = { member_id: this.currentMember.id }
          
          this.questions = await this.$services.perspective.listQuestions(this.projectId, params)
        } else {
          // Members see questions they need to answer
          console.log('Loading questions as member')
          this.questions = await this.$services.perspective.getQuestionsForMember(
            this.projectId,
            this.currentMember.id
          )
        }
        console.log('Successfully loaded', this.questions.length, 'questions')
        this.buildAnswerFilterOptions()
        this.applyFilters()
      } catch (error) {
        console.error('Error loading questions:', error)
        let errorMessage = this.$t('perspectives.failedToLoadQuestions')

        if (error && error.response && error.response.data) {
          if (typeof error.response.data === 'string') {
            errorMessage = error.response.data
          } else if (error.response.data.error) {
            errorMessage = error.response.data.error
          } else if (error.response.data.detail) {
            errorMessage = error.response.data.detail
          }
        } else if (error && error.message) {
          errorMessage = error.message
        }

        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: errorMessage
        })
      } finally {
        this.loading = false
      }
    },

    async loadStats() {
      this.statsLoading = true
      try {
        this.projectStats = await this.$services.perspective.getProjectStats(this.projectId)
      } catch (error) {
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: this.$t('perspectives.failedToLoadStatistics')
        })
        console.error(error)
      } finally {
        this.statsLoading = false
      }
    },

    editQuestion(question) {
      this.editingQuestion = question
      this.showCreateDialog = true
    },

    deleteQuestion(question) {
      this.questionToDelete = question
      this.showDeleteDialog = true
    },

    async confirmDelete() {
      if (!this.questionToDelete) return

      try {
        await this.$services.perspective.deleteQuestion(this.projectId, this.questionToDelete.id)
        this.$store.dispatch('notification/setNotification', {
          color: 'success',
          text: this.$t('perspectives.questionDeletedSuccess')
        })
        await this.loadQuestions()
        if (this.isProjectAdmin) {
          await this.loadStats()
        }
      } catch (error) {
        console.error('Delete error:', error)

        // Check if it's a database connection error
        const isDatabaseError = this.isDatabaseConnectionError(error)

        if (isDatabaseError) {
          // Show database connection error dialog
          this.showDatabaseErrorDialog = true
        } else {
          // Show generic error notification
          this.$store.dispatch('notification/setNotification', {
            color: 'error',
            text: this.$t('perspectives.failedToDeleteQuestion')
          })
        }
      } finally {
        this.showDeleteDialog = false
        this.questionToDelete = null
      }
    },

    isDatabaseConnectionError(error) {
      // Check various indicators of database connection issues
      if (!error) return false

      // Check for network errors (no response from server)
      if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
        return true
      }

      // Check for connection refused or timeout errors
      if (error.message && (
        error.message.includes('ECONNREFUSED') ||
        error.message.includes('timeout') ||
        error.message.includes('Connection refused') ||
        error.message.includes('ERR_NETWORK')
      )) {
        return true
      }

      // Check HTTP status codes that indicate server/database issues
      if (error.response) {
        const status = error.response.status
        // 500: Internal Server Error (could be database)
        // 502: Bad Gateway (server down)
        // 503: Service Unavailable (database down)
        // 504: Gateway Timeout (database timeout)
        if (status === 500 || status === 502 || status === 503 || status === 504) {
          return true
        }

        // Check response data for database-specific error messages
        if (error.response.data) {
          const errorData = error.response.data
          const errorText = typeof errorData === 'string' ? errorData : JSON.stringify(errorData)

          if (errorText.includes('database') ||
              errorText.includes('connection') ||
              errorText.includes('DatabaseError') ||
              errorText.includes('OperationalError') ||
              errorText.includes('InterfaceError')) {
            return true
          }
        }
      }

      return false
    },

    async saveQuestion(questionData) {
      this.formLoading = true
      try {
        if (this.editingQuestion) {
          await this.$services.perspective.updateQuestion(
            this.projectId,
            this.editingQuestion.id,
            questionData
          )
          this.$store.dispatch('notification/setNotification', {
            color: 'success',
            text: this.$t('perspectives.questionUpdatedSuccess')
          })
        } else {
          // Reload questions to get the most up-to-date data before calculating order
          await this.loadQuestions()
          
          // Set the next available order for new questions
          if (!questionData.order || questionData.order === 1) {
            questionData.order = this.nextOrder
          }
          console.log('Creating question with order:', questionData.order)
          
          const createdQuestion = await this.$services.perspective.createQuestion(this.projectId, questionData)
          console.log('Question created successfully with ID:', createdQuestion.id)
          
          this.$store.dispatch('notification/setNotification', {
            color: 'success',
            text: this.$t('perspectives.questionCreatedSuccess')
          })
        }

        console.log('Reloading questions after save...')
        await this.loadQuestions()
        
        if (this.isProjectAdmin) {
          await this.loadStats()
        }
        this.closeDialog()
      } catch (error) {
        console.error('Error saving question:', error)
        let errorMessage = this.$t('perspectives.failedToSaveQuestion')

        if (error && error.response && error.response.data) {
          if (typeof error.response.data === 'string') {
            errorMessage = error.response.data
          } else if (error.response.data.error) {
            errorMessage = error.response.data.error
          } else if (error.response.data.detail) {
            errorMessage = error.response.data.detail
          } else if (error.response.data.non_field_errors) {
            errorMessage = error.response.data.non_field_errors.join(', ')
          }
        } else if (error && error.message) {
          errorMessage = error.message
        }

        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: errorMessage
        })
      } finally {
        this.formLoading = false
      }
    },

    async submitAnswer(answerData) {
      try {
        await this.$services.perspective.createAnswer(this.projectId, answerData)
        this.$store.dispatch('notification/setNotification', {
          color: 'success',
          text: this.$t('perspectives.answerSubmittedSuccess')
        })
        await this.loadQuestions()
      } catch (error) {
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: this.$t('perspectives.failedToSubmitAnswer')
        })
        console.error(error)
      }
    },

    async cancelAnswer(answerId) {
      try {
        await this.$services.perspective.deleteAnswer(this.projectId, answerId)
        this.$store.dispatch('notification/setNotification', {
          color: 'success',
          text: 'Resposta cancelada com sucesso'
        })
        await this.loadQuestions()
      } catch (error) {
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Erro ao cancelar resposta'
        })
        console.error(error)
      }
    },

    closeDialog() {
      this.showCreateDialog = false
      this.editingQuestion = null
    },

    // Method for testing database connection error (can be removed in production)
    testDatabaseError() {
      this.showDatabaseErrorDialog = true
    },

    // Filter and Search Methods
    buildAnswerFilterOptions() {
      if (!this.isProjectAdmin) {
        this.answerFilterOptions = []
        return
      }

      const uniqueAnswers = new Set()
      
      this.questions.forEach(question => {
        if (question.answers && question.answers.length > 0) {
          question.answers.forEach(answer => {
            if (answer.content && answer.content.trim()) {
              uniqueAnswers.add(answer.content.trim())
            }
          })
        }
      })

      this.answerFilterOptions = Array.from(uniqueAnswers)
        .sort()
        .map(answer => ({
          text: answer.length > 50 ? answer.substring(0, 50) + '...' : answer,
          value: answer
        }))
    },

    applyFilters() {
      let filtered = [...this.questions]

      // Apply search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(question =>
          question.text.toLowerCase().includes(query)
        )
      }

      // Apply answer filter
      if (this.filters.answerFilter) {
        filtered = filtered.filter(question => {
          if (!question.answers || question.answers.length === 0) {
            return false
          }
          return question.answers.some(answer =>
            answer.content && answer.content.trim() === this.filters.answerFilter
          )
        })
      }

      // Apply question type filter
      if (this.filters.questionType) {
        filtered = filtered.filter(question =>
          question.questionType === this.filters.questionType
        )
      }

      // Apply data type filter
      if (this.filters.dataType) {
        filtered = filtered.filter(question =>
          question.dataType === this.filters.dataType
        )
      }

      // Apply required filter
      if (this.filters.isRequired !== null) {
        filtered = filtered.filter(question =>
          question.isRequired === this.filters.isRequired
        )
      }

      // Apply answer count filter
      if (this.filters.answerCount) {
        filtered = filtered.filter(question => {
          const count = question.answerCount
          switch (this.filters.answerCount) {
            case 'none':
              return count === 0
            case 'few':
              return count >= 1 && count <= 5
            case 'many':
              return count >= 6
            default:
              return true
          }
        })
      }

      // Apply sorting
      filtered.sort((a, b) => {
        let aValue, bValue

        switch (this.sortBy) {
          case 'text':
            aValue = a.text.toLowerCase()
            bValue = b.text.toLowerCase()
            break
          case 'questionType':
            aValue = a.questionType
            bValue = b.questionType
            break
          case 'dataType':
            aValue = a.dataType || ''
            bValue = b.dataType || ''
            break
          case 'answerCount':
            aValue = a.answerCount
            bValue = b.answerCount
            break
          case 'createdAt':
            aValue = new Date(a.createdAt)
            bValue = new Date(b.createdAt)
            break
          case 'order':
          default:
            aValue = a.order
            bValue = b.order
            break
        }

        if (aValue < bValue) {
          return this.sortOrder === 'asc' ? -1 : 1
        }
        if (aValue > bValue) {
          return this.sortOrder === 'asc' ? 1 : -1
        }
        return 0
      })

      this.filteredQuestions = filtered
    },

    clearFilters() {
      this.searchQuery = ''
      this.filters = {
        questionType: null,
        dataType: null,
        isRequired: null,
        answerCount: null,
        answerFilter: null
      }
      this.sortBy = 'order'
      this.sortOrder = 'asc'
      this.applyFilters()
    }
  }
}
</script>
