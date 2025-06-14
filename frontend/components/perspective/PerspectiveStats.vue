<template>
  <div>
    <v-progress-linear v-if="loading" indeterminate class="mb-4" />

    <div v-else-if="stats">
      <!-- Overview Cards -->
      <v-row class="mb-6">
        <v-col cols="12" md="3">
          <v-card>
            <v-card-text class="text-center">
              <v-icon size="48" color="primary">{{ mdiHelpCircle }}</v-icon>
              <h2 class="text-h4 mt-2">{{ stats.totalQuestions }}</h2>
              <p class="text-body-1">Total Questions</p>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="3">
          <v-card>
            <v-card-text class="text-center">
              <v-icon size="48" color="success">{{ mdiCheckCircle }}</v-icon>
              <h2 class="text-h4 mt-2">{{ stats.totalAnswers }}</h2>
              <p class="text-body-1">Total Answers</p>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="3">
          <v-card>
            <v-card-text class="text-center">
              <v-icon size="48" color="info">{{ mdiChartBar }}</v-icon>
              <h2 class="text-h4 mt-2">{{ stats.questionsWithAnswers }}</h2>
              <p class="text-body-1">Questions with Answers</p>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="3">
          <v-card>
            <v-card-text class="text-center">
              <v-icon size="48" color="warning">{{ mdiPercent }}</v-icon>
              <h2 class="text-h4 mt-2">{{ responseRate }}%</h2>
              <p class="text-body-1">Response Rate</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Detailed Question Statistics -->
      <v-card>
        <v-card-title>
          <h3>Question Details</h3>
        </v-card-title>
        <v-card-text>
          <div v-for="question in stats.questions" :key="question.id" class="mb-6">
            <v-card outlined>
              <v-card-subtitle>
                <div class="d-flex align-center">
                  <span class="text-h6">{{ question.text }}</span>
                  <v-spacer />
                  <v-chip small>
                    {{ question.questionType === 'open' ? 'Open Text' : 'Multiple Choice' }}
                  </v-chip>
                </div>
              </v-card-subtitle>

              <v-card-text>
                <div class="d-flex align-center mb-3">
                  <v-icon color="info" class="mr-2">{{ mdiAccount }}</v-icon>
                  <span>{{ question.answerCount }} responses</span>
                </div>

                <!-- Multiple choice options breakdown -->
                <div v-if="question.questionType === 'closed' && question.options.length > 0">
                  <h4 class="mb-3">Answer Distribution:</h4>
                  <div v-for="option in question.options" :key="option.id" class="mb-2">
                    <div class="d-flex align-center">
                      <span class="text-body-2 mr-3" style="min-width: 200px;">
                        {{ option.text }}
                      </span>
                      <v-progress-linear
                        :value="getOptionPercentage(option, question)"
                        height="20"
                        class="flex-grow-1 mr-3"
                        :color="getProgressColor(getOptionPercentage(option, question))"
                      >
                        <span class="white--text text-caption">
                          {{ option.answerCount }}
                        </span>
                      </v-progress-linear>
                      <span class="text-caption" style="min-width: 40px;">
                        {{ getOptionPercentage(option, question).toFixed(1) }}%
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Open text responses summary -->
                <div v-else-if="question.questionType === 'open'">
                  <p class="text-body-2">
                    This is an open text question. {{ question.answerCount }} text responses have been submitted.
                  </p>
                </div>
              </v-card-text>
            </v-card>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <v-alert v-else type="info" outlined>
      No statistics available.
    </v-alert>
  </div>
</template>

<script>
import { mdiHelpCircle, mdiCheckCircle, mdiChartBar, mdiPercent, mdiAccount } from '@mdi/js'

export default {
  props: {
    stats: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      mdiHelpCircle,
      mdiCheckCircle,
      mdiChartBar,
      mdiPercent,
      mdiAccount
    }
  },

  computed: {
    responseRate() {
      if (!this.stats || this.stats.totalQuestions === 0) {
        return 0
      }
      return ((this.stats.questionsWithAnswers / this.stats.totalQuestions) * 100).toFixed(1)
    }
  },

  methods: {
    getOptionPercentage(option, question) {
      if (question.answerCount === 0) {
        return 0
      }
      return (option.answerCount / question.answerCount) * 100
    },

    getProgressColor(percentage) {
      if (percentage >= 70) return 'success'
      if (percentage >= 40) return 'warning'
      return 'error'
    }
  }
}
</script>
