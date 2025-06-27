<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="questions"
      :loading="loading"
      class="elevation-1"
      :items-per-page="10"
    >
      <template #[`item.data_type`]="{ item }">
        <v-chip
          v-if="item.dataType"
          :color="item.dataType === 'string' ? 'purple' : 'orange'"
          text-color="white"
          small
        >
          {{ item.dataType === 'string' ? 'String' : 'Integer' }}
        </v-chip>
        <span v-else class="grey--text">-</span>
      </template>

      <template #[`item.question_type`]="{ item }">
        <v-chip
          :color="item.questionType === 'open' ? 'blue' : 'green'"
          text-color="white"
          small
        >
          {{ item.questionType === 'open' ? 'Open Text' : 'Multiple Choice' }}
        </v-chip>
      </template>

      <template #[`item.is_required`]="{ item }">
        <v-icon :color="item.isRequired ? 'success' : 'grey'">
          {{ item.isRequired ? mdiCheck : mdiClose }}
        </v-icon>
      </template>

      <template #[`item.answer_count`]="{ item }">
        <v-btn
          small
          color="primary"
          outlined
          :disabled="item.answerCount === 0"
          @click="viewAnswers(item)"
        >
          <v-icon left small>mdi-eye</v-icon>
          {{ item.answerCount }} answers
        </v-btn>
      </template>

      <template #[`item.actions`]="{ item }">
        <v-btn icon small @click="$emit('edit', item)">
          <v-icon>{{ mdiPencil }}</v-icon>
        </v-btn>
        <v-btn icon small color="error" @click="$emit('delete', item)">
          <v-icon>{{ mdiDelete }}</v-icon>
        </v-btn>
      </template>

      <template #[`item.text`]="{ item }">
        <div class="text-truncate" style="max-width: 300px;">
          {{ item.text }}
        </div>
      </template>
    </v-data-table>

    <!-- Answers Dialog -->
    <v-dialog v-model="showAnswersDialog" max-width="900px" scrollable>
      <v-card class="answers-dialog">
        <!-- Header with gradient background -->
        <v-card-title class="answers-header white--text pa-6">
          <div>
            <h2 class="text-h5 font-weight-bold mb-1">Item Responses</h2>
            <p class="mb-0 text-body-2 white--text" style="opacity: 0.9;">
              View all responses submitted for this item
            </p>
          </div>
        </v-card-title>
        
        <!-- Item Info Card -->
        <v-card-text class="pa-0">
          <v-card 
            v-if="selectedQuestionAnswers" 
            flat 
            class="ma-4 mb-2" 
            color="blue-grey lighten-5"
            outlined
          >
            <v-card-text class="pa-4">
              <div class="d-flex align-start">
                <v-icon color="blue-grey darken-2" class="mr-3 mt-1">mdi-help-circle-outline</v-icon>
                <div class="flex-grow-1">
                  <h3 class="text-subtitle-1 font-weight-bold blue-grey--text text--darken-3 mb-2">
                    Item
                  </h3>
                  <p class="text-body-1 mb-3">{{ selectedQuestionAnswers.question_text }}</p>
                  
                  <div class="d-flex align-center">
                    <v-chip
                      :color="selectedQuestionAnswers.question_type === 'open' ? 'blue' : 'green'"
                      text-color="white"
                      small
                      class="mr-3"
                    >
                      <v-icon left small>
                        {{ selectedQuestionAnswers.question_type === 'open' ? 'mdi-text' : 'mdi-format-list-bulleted' }}
                      </v-icon>
                      {{ selectedQuestionAnswers.question_type === 'open' ? 'Open Text' : 'Multiple Choice' }}
                    </v-chip>
                    
                    <v-chip color="primary" text-color="white" small>
                      <v-icon left small>mdi-counter</v-icon>
                      {{ selectedQuestionAnswers.total_answers }} 
                      {{ selectedQuestionAnswers.total_answers === 1 ? 'Response' : 'Responses' }}
                    </v-chip>
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-card-text>

        <!-- Responses Content -->
        <v-card-text class="px-4 pb-4" style="max-height: 400px; overflow-y: auto;">
          <!-- Loading State -->
          <div v-if="loadingAnswers" class="text-center py-8">
            <v-progress-circular 
              indeterminate 
              color="primary" 
              size="48"
              width="4"
            />
            <p class="mt-4 text-h6 grey--text">Loading responses...</p>
          </div>

          <!-- Responses List -->
          <div v-else-if="selectedQuestionAnswers && selectedQuestionAnswers.answers.length > 0">
            <v-row>
              <v-col
                v-for="answer in selectedQuestionAnswers.answers"
                :key="answer.id"
                cols="12"
                class="py-2"
              >
                <v-card 
                  class="answer-card" 
                  elevation="2"
                  :class="answer.type === 'text' ? 'text-answer' : 'choice-answer'"
                >
                  <v-card-text class="pa-4">
                    <!-- Answer Header -->
                    <div class="d-flex align-center justify-space-between mb-3">
                      <v-chip
                        :color="answer.type === 'text' ? 'blue' : 'green'"
                        text-color="white"
                        small
                        class="font-weight-bold"
                      >
                        <v-icon left small>
                          {{ answer.type === 'text' ? 'mdi-text-box' : 'mdi-check-circle' }}
                        </v-icon>
                        {{ answer.type === 'text' ? 'Text Response' : 'Selected Choice' }}
                      </v-chip>
                      
                      <span class="grey--text text--darken-1 caption font-weight-medium">
                        <v-icon small class="mr-1">mdi-clock-outline</v-icon>
                        {{ formatDate(answer.created_at) }}
                      </span>
                    </div>
                    
                    <!-- Answer Content -->
                    <div class="answer-content-modern">
                      <v-icon 
                        :color="answer.type === 'text' ? 'blue' : 'green'" 
                        class="quote-icon"
                        small
                      >
                        mdi-format-quote-open
                      </v-icon>
                      <div class="answer-text">
                        {{ answer.content }}
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-8">
            <v-avatar size="80" color="grey lighten-3" class="mb-4">
              <v-icon size="40" color="grey">mdi-comment-off-outline</v-icon>
            </v-avatar>
            <h3 class="text-h6 grey--text text--darken-1 mb-2">No Responses Yet</h3>
            <p class="grey--text">This item hasn't received any responses from annotators.</p>
          </div>
        </v-card-text>

        <!-- Footer Actions -->
        <v-divider />
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn 
            color="primary" 
            large
            @click="showAnswersDialog = false"
            class="px-6"
          >
            <v-icon left>mdi-close</v-icon>
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mdiPencil, mdiDelete, mdiCheck, mdiClose } from '@mdi/js'

export default {
  props: {
    questions: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      mdiPencil,
      mdiDelete,
      mdiCheck,
      mdiClose,
      showAnswersDialog: false,
      selectedQuestionAnswers: null,
      loadingAnswers: false,
      headers: [
        {
          text: 'Order',
          value: 'order',
          width: '80px'
        },
        {
          text: 'Item',
          value: 'text',
          sortable: false
        },
        {
          text: 'Data Type',
          value: 'data_type',
          width: '120px'
        },
        {
          text: 'Item Type',
          value: 'question_type',
          width: '150px'
        },
        {
          text: 'Required',
          value: 'is_required',
          width: '100px'
        },
        {
          text: 'Answers',
          value: 'answer_count',
          width: '120px'
        },
        {
          text: 'Actions',
          value: 'actions',
          sortable: false,
          width: '120px'
        }
      ]
    }
  },

  methods: {
    async viewAnswers(question) {
      this.showAnswersDialog = true
      this.loadingAnswers = true
      this.selectedQuestionAnswers = null

      try {
        // Get project ID from parent component or route
        const projectId = this.$route.params.id
        const answersData = await this.$services.perspective.getQuestionAnswers(projectId, question.id)
        this.selectedQuestionAnswers = answersData
      } catch (error) {
        console.error('Error loading answers:', error)
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Erro ao carregar respostas'
        })
      } finally {
        this.loadingAnswers = false
      }
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('pt-PT', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
/* Dialog Header Gradient */
.answers-header {
  background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
  position: relative;
}

.answers-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  pointer-events: none;
}

/* Answer Cards */
.answer-card {
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
  position: relative;
  overflow: hidden;
}

.answer-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.text-answer {
  border-left-color: #2196f3;
}

.choice-answer {
  border-left-color: #4caf50;
}

/* Modern Answer Content */
.answer-content-modern {
  position: relative;
  background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 16px 20px;
  border: 1px solid #e0e0e0;
}

.quote-icon {
  position: absolute;
  top: 8px;
  left: 8px;
  opacity: 0.3;
}

.answer-text {
  word-wrap: break-word;
  white-space: pre-wrap;
  font-family: 'Roboto', sans-serif;
  line-height: 1.6;
  font-size: 14px;
  color: #424242;
  margin-left: 20px;
  position: relative;
}

/* Scrollbar Styling */
.v-card__text::-webkit-scrollbar {
  width: 6px;
}

.v-card__text::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.v-card__text::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.v-card__text::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Animation for loading */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.answer-card {
  animation: fadeInUp 0.4s ease-out;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .answers-header {
    padding: 16px !important;
  }
  
  .answer-content-modern {
    padding: 12px 16px;
  }
  
  .answer-text {
    margin-left: 16px;
    font-size: 13px;
  }
}
</style>
