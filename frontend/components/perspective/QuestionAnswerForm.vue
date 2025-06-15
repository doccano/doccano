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
              <!-- Data type hint -->
              <v-alert
                v-if="question.dataType"
                type="info"
                outlined
                dense
                class="mb-3"
              >
                <v-icon left small>mdi-information</v-icon>
                {{ getDataTypeMessage(question.dataType) }}
              </v-alert>
              
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
                            <p class="mt-2 text-body-1">You have already answered this item.</p>
            
            <v-btn
              color="warning"
              outlined
              class="mt-3"
              :loading="cancelling[question.id]"
              @click="cancelAnswer(question)"
            >
              <v-icon left>mdi-undo</v-icon>
              Cancelar Resposta
            </v-btn>
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
      cancelling: {},
      textRules: [
        v => !!v || 'Answer is required',
        v => (!v || v.length >= 1) || 'Answer must be at least 1 character'
      ],
      choiceRules: [
        v => v !== null && v !== undefined || 'Please select an option'
      ]
    }
  },

  methods: {
    getDataTypeMessage(dataType) {
      if (dataType === 'string') {
        return 'This answer should be text'
      } else if (dataType === 'integer') {
        return 'This answer should be a number'
      }
      return ''
    },

    canSubmit(question) {
      const answer = this.answers[question.id]
      
      if (question.isRequired) {
        if (question.isOpen) {
          return answer && answer.trim().length >= 1
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
    },

    async cancelAnswer(question) {
      if (!question.userAnswerId) {
        console.error('No answer ID found for question:', question.id)
        return
      }

      // Set cancelling state
      this.$set(this.cancelling, question.id, true)

      try {
        await this.$emit('cancel-answer', question.userAnswerId)
      } catch (error) {
        console.error('Error cancelling answer:', error)
      } finally {
        this.$set(this.cancelling, question.id, false)
      }
    }
  }
}
</script>
