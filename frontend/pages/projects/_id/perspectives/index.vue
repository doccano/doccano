<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2>{{ $t('perspectives.perspectives') }}</h2>
            <v-spacer />
            <v-btn
              v-if="isProjectAdmin"
              color="primary"
              @click="showCreateDialog = true"
            >
              <v-icon left>{{ mdiPlus }}</v-icon>
              {{ $t('perspectives.addQuestion') }}
            </v-btn>
          </v-card-title>

          <v-tabs v-model="activeTab" background-color="transparent">
            <v-tab key="questions">{{ $t('perspectives.questions') }}</v-tab>
            <v-tab v-if="isProjectAdmin" key="statistics">{{ $t('perspectives.statistics') }}</v-tab>
          </v-tabs>

          <v-tabs-items v-model="activeTab">
            <!-- Questions Tab -->
            <v-tab-item key="questions">
              <v-card-text>
                <div v-if="isProjectAdmin">
                  <h3 class="mb-4">{{ $t('perspectives.manageQuestions') }}</h3>
                  <question-list
                    :questions="questions"
                    :loading="loading"
                    @edit="editQuestion"
                    @delete="deleteQuestion"
                    @delete-all="deleteAllQuestions"
                  />
                </div>
                <div v-else>
                  <h3 class="mb-4">{{ $t('perspectives.answerQuestions') }}</h3>
                  <question-answer-form
                    :questions="questions"
                    :loading="loading"
                    @answer="submitAnswer"
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
        :next-order="getNextOrder()"
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

    <!-- Delete All Confirmation Dialog -->
    <v-dialog v-model="showDeleteAllDialog" max-width="500px">
      <v-card>
        <v-card-title class="headline error--text">
          <v-icon color="error" class="mr-2">{{ mdiDelete }}</v-icon>
          {{ $t('perspectives.confirmDeleteAll') }}
        </v-card-title>
        <v-card-text>
          <v-alert type="warning" outlined class="mb-3">
            {{ $t('perspectives.deleteAllQuestionsWarning') }}
          </v-alert>
          <p>{{ $t('perspectives.deleteAllQuestionsConfirm') }}</p>
          <p class="font-weight-bold">{{ $t('perspectives.thisActionCannotBeUndone') }}</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showDeleteAllDialog = false">{{ $t('generic.cancel') }}</v-btn>
          <v-btn color="error" @click="confirmDeleteAll">{{ $t('perspectives.deleteAll') }}</v-btn>
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
import { mdiPlus, mdiDelete } from '@mdi/js'
import QuestionList from '@/components/perspective/QuestionList.vue'
import QuestionAnswerForm from '@/components/perspective/QuestionAnswerForm.vue'
import QuestionForm from '@/components/perspective/QuestionForm.vue'
import PerspectiveStats from '@/components/perspective/PerspectiveStats.vue'

export default {
  components: {
    QuestionList,
    QuestionAnswerForm,
    QuestionForm,
    PerspectiveStats
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      mdiPlus,
      mdiDelete,
      activeTab: 0,
      questions: [],
      projectStats: null,
      loading: false,
      statsLoading: false,
      formLoading: false,
      showCreateDialog: false,
      showDeleteDialog: false,
      showDeleteAllDialog: false,
      showDatabaseErrorDialog: false,
      editingQuestion: null,
      questionToDelete: null,
      isProjectAdmin: false,
      currentMember: null
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    ...mapGetters('auth', ['getUserId']),

    projectId() {
      return this.$route.params.id
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
          this.questions = await this.$services.perspective.listQuestions(this.projectId, {
            member_id: this.currentMember.id
          })
        } else {
          // Members see questions they need to answer
          console.log('Loading questions as member')
          this.questions = await this.$services.perspective.getQuestionsForMember(
            this.projectId,
            this.currentMember.id
          )
        }
        console.log('Loaded questions:', this.questions)
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

    getNextOrder() {
      if (this.questions.length === 0) {
        return 1
      }
      const maxOrder = Math.max(...this.questions.map(q => q.order))
      return maxOrder + 1
    },

    deleteQuestion(question) {
      this.questionToDelete = question
      this.showDeleteDialog = true
    },

    deleteAllQuestions() {
      this.showDeleteAllDialog = true
    },

    async confirmDelete() {
      if (!this.questionToDelete) return

      const questionToDeleteId = this.questionToDelete.id
      let deleteSuccessful = false

      try {
        await this.$services.perspective.deleteQuestion(this.projectId, questionToDeleteId)
        deleteSuccessful = true
        console.log('Question deleted successfully:', questionToDeleteId)

        // Show success notification immediately after successful delete
        this.$store.dispatch('notification/setNotification', {
          color: 'success',
          text: this.$t('perspectives.questionDeletedSuccess')
        })

        // Try to reload data, but don't let errors here affect the success notification
        try {
          await this.loadQuestions()
          if (this.isProjectAdmin) {
            await this.loadStats()
          }
        } catch (reloadError) {
          console.error('Error reloading after delete:', reloadError)
          // Don't show error to user since the delete was successful
        }

      } catch (error) {
        console.error('Delete error:', error)
        console.error('Error details:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message
        })

        // Check if the operation actually succeeded despite the error
        if (error.response?.status === 502 ||
            (error.response?.data && typeof error.response.data === 'object' && error.response.data.message)) {
          console.log('Delete operation may have succeeded despite error, checking...')

          // Try to reload questions to see if the question was actually deleted
          try {
            await this.loadQuestions()
            const questionStillExists = this.questions.some(q => q.id === questionToDeleteId)

            if (!questionStillExists) {
              // Question was deleted successfully
              deleteSuccessful = true
              this.$store.dispatch('notification/setNotification', {
                color: 'success',
                text: this.$t('perspectives.questionDeletedSuccess')
              })
              if (this.isProjectAdmin) {
                await this.loadStats()
              }
            }
          } catch (reloadError) {
            console.error('Error reloading questions after potential success:', reloadError)
          }
        }

        // Only show error if delete was not successful
        if (!deleteSuccessful) {
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
        }
      } finally {
        this.showDeleteDialog = false
        this.questionToDelete = null
      }
    },

    async confirmDeleteAll() {
      try {
        const response = await this.$services.perspective.deleteAllQuestions(this.projectId)
        console.log('Delete all response:', response)

        this.$store.dispatch('notification/setNotification', {
          color: 'success',
          text: this.$t('perspectives.allQuestionsDeletedSuccess')
        })
        await this.loadQuestions()
        if (this.isProjectAdmin) {
          await this.loadStats()
        }
      } catch (error) {
        console.error('Delete all error:', error)
        console.error('Error details:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message
        })

        // Check if the operation actually succeeded despite the error
        // This can happen with 502 errors that are actually successful operations
        if (error.response?.status === 502 ||
            (error.response?.data && typeof error.response.data === 'object' && error.response.data.message)) {
          console.log('Operation may have succeeded despite error, checking...')

          // Try to reload questions to see if they were actually deleted
          try {
            await this.loadQuestions()
            if (this.questions.length === 0) {
              // Questions were deleted successfully
              this.$store.dispatch('notification/setNotification', {
                color: 'success',
                text: this.$t('perspectives.allQuestionsDeletedSuccess')
              })
              if (this.isProjectAdmin) {
                await this.loadStats()
              }
              this.showDeleteAllDialog = false
              return
            }
          } catch (reloadError) {
            console.error('Error reloading questions:', reloadError)
          }
        }

        // Check if it's a database connection error
        const isDatabaseError = this.isDatabaseConnectionError(error)

        if (isDatabaseError) {
          // Show database connection error dialog
          this.showDatabaseErrorDialog = true
        } else {
          // Show generic error notification
          this.$store.dispatch('notification/setNotification', {
            color: 'error',
            text: this.$t('perspectives.failedToDeleteAllQuestions')
          })
        }
      } finally {
        this.showDeleteAllDialog = false
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
        // 502: Bad Gateway (server down) - but only if it's actually a server error
        // 503: Service Unavailable (database down)
        // 504: Gateway Timeout (database timeout)
        if (status === 500 || status === 503 || status === 504) {
          return true
        }

        // For 502, check if it's actually a server error or just a response parsing issue
        if (status === 502) {
          // Only treat as database error if there's no successful response data
          if (!error.response.data || (typeof error.response.data === 'string' && error.response.data.includes('error'))) {
            return true
          }
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
          // Set the next available order for new questions
          if (!questionData.order || questionData.order === 1) {
            questionData.order = this.getNextOrder()
          }
          console.log('Creating question with data:', questionData)
          await this.$services.perspective.createQuestion(this.projectId, questionData)
          this.$store.dispatch('notification/setNotification', {
            color: 'success',
            text: this.$t('perspectives.questionCreatedSuccess')
          })
        }

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

    closeDialog() {
      this.showCreateDialog = false
      this.editingQuestion = null
    },

    // Method for testing database connection error (can be removed in production)
    testDatabaseError() {
      this.showDatabaseErrorDialog = true
    }
  }
}
</script>
