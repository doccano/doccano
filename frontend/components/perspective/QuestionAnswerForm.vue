<template>
  <div>
    <v-alert
      v-if="questions.length === 0 && !loading"
      type="info"
      outlined
    >
      No questions available to answer at this time.
    </v-alert>

    <div v-else>
      <v-card
        v-for="question in questions"
        :key="question.id"
        class="mb-4"
        outlined
      >
        <v-card-text>
          <div class="d-flex align-center mb-3">
            <h3 class="text-h6">{{ question.text }}</h3>
            <v-spacer />
            <v-chip
              :color="question.isRequired ? 'error' : 'info'"
              text-color="white"
              small
            >
              {{ question.isRequired ? 'Required' : 'Optional' }}
            </v-chip>
            <v-chip
              v-if="question.userAnswered"
              color="success"
              text-color="white"
              small
              class="ml-2"
            >
              <v-icon left small>{{ mdiCheck }}</v-icon>
              Answered
            </v-chip>
          </div>

          <div v-if="!question.userAnswered">
            <!-- Open text question -->
            <div v-if="question.isOpen">
              <v-textarea
                v-model="answers[question.id]"
                label="Your answer"
                outlined
                rows="3"
                :rules="question.isRequired ? textRules : []"
              />
            </div>

            <!-- Multiple choice question -->
            <div v-else-if="question.isClosed">
              <v-radio-group
                v-model="answers[question.id]"
                :rules="question.isRequired ? choiceRules : []"
              >
                <v-radio
                  v-for="option in question.options"
                  :key="option.id"
                  :label="option.text"
                  :value="option.id"
                />
              </v-radio-group>
            </div>

            <v-btn
              color="primary"
              :loading="submitting[question.id]"
              :disabled="!canSubmit(question)"
              @click="submitAnswer(question)"
            >
              Submit Answer
            </v-btn>
          </div>

          <div v-else class="text-center py-4">
            <v-icon color="success" size="48">{{ mdiCheckCircle }}</v-icon>
            <p class="mt-2 text-body-1">You have already answered this question.</p>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <v-progress-linear v-if="loading" indeterminate />
  </div>
</template>

<script>
import { mdiCheck, mdiCheckCircle } from '@mdi/js'

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
      mdiCheck,
      mdiCheckCircle,
      answers: {},
      submitting: {},
      textRules: [
        v => !!v || 'Answer is required',
        v => v.length >= 5 || 'Answer must be at least 5 characters'
      ],
      choiceRules: [
        v => v !== null && v !== undefined || 'Please select an option'
      ]
    }
  },

  methods: {
    canSubmit(question) {
      const answer = this.answers[question.id]
      
      if (question.isRequired) {
        if (question.isOpen) {
          return answer && answer.trim().length >= 5
        } else if (question.isClosed) {
          return answer !== null && answer !== undefined
        }
      } else {
        // Optional questions can be submitted even without answers
        return true
      }
      
      return false
    },

    async submitAnswer(question) {
      const answer = this.answers[question.id]
      
      // Set submitting state
      this.$set(this.submitting, question.id, true)

      try {
        const payload = {
          question: question.id
        }

        if (question.isOpen) {
          payload.text_answer = answer || ''
        } else if (question.isClosed) {
          payload.selected_option = answer
        }

        await this.$emit('answer', payload)
        
        // Clear the answer from local state
        this.$delete(this.answers, question.id)
        
      } catch (error) {
        console.error('Error submitting answer:', error)
      } finally {
        this.$set(this.submitting, question.id, false)
      }
    }
  }
}
</script>
