<template>
  <v-card>
    <v-card-title>
      {{ isEditing ? 'Edit Question' : 'Create Question' }}
    </v-card-title>

    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-textarea
          v-model="formData.text"
          label="Question Text"
          :rules="textRules"
          required
          rows="3"
          outlined
        />

        <v-select
          v-model="formData.question_type"
          :items="questionTypes"
          label="Question Type"
          :rules="typeRules"
          required
          outlined
        />

        <v-text-field
          v-model.number="formData.order"
          label="Order"
          type="number"
          :rules="orderRules"
          required
          outlined
        />

        <v-checkbox
          v-model="formData.is_required"
          label="Required"
        />

        <!-- Options for closed questions -->
        <div v-if="formData.question_type === 'closed'">
          <v-subheader>Answer Options</v-subheader>
          
          <div v-for="(option, index) in formData.options" :key="index" class="mb-2">
            <v-row>
              <v-col cols="8">
                <v-text-field
                  v-model="option.text"
                  :label="`Option ${index + 1}`"
                  :rules="optionRules"
                  outlined
                  dense
                />
              </v-col>
              <v-col cols="2">
                <v-text-field
                  v-model.number="option.order"
                  label="Order"
                  type="number"
                  outlined
                  dense
                />
              </v-col>
              <v-col cols="2">
                <v-btn
                  icon
                  color="error"
                  @click="removeOption(index)"
                  :disabled="formData.options.length <= 2"
                >
                  <v-icon>{{ mdiDelete }}</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </div>

          <v-btn
            text
            color="primary"
            @click="addOption"
            :disabled="formData.options.length >= 10"
          >
            <v-icon left>{{ mdiPlus }}</v-icon>
            Add Option
          </v-btn>
        </div>
      </v-form>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn text @click="$emit('cancel')">Cancel</v-btn>
      <v-btn
        color="primary"
        :loading="loading"
        :disabled="!valid"
        @click="save"
      >
        {{ isEditing ? 'Update' : 'Create' }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mdiPlus, mdiDelete } from '@mdi/js'

export default {
  props: {
    question: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    },
    nextOrder: {
      type: Number,
      default: 1
    }
  },

  data() {
    return {
      mdiPlus,
      mdiDelete,
      valid: false,
      formData: {
        text: '',
        question_type: 'open',
        is_required: true,
        order: 1,
        options: []
      },
      questionTypes: [
        { text: 'Open Text', value: 'open' },
        { text: 'Multiple Choice', value: 'closed' }
      ],
      textRules: [
        v => !!v || 'Question text is required',
        v => (!v || v.length >= 10) || 'Question must be at least 10 characters'
      ],
      typeRules: [
        v => !!v || 'Question type is required'
      ],
      orderRules: [
        v => v !== null && v !== undefined || 'Order is required',
        v => v > 0 || 'Order must be greater than 0'
      ],
      optionRules: [
        v => !!v || 'Option text is required',
        v => (!v || v.length >= 1) || 'Option must not be empty'
      ]
    }
  },

  computed: {
    isEditing() {
      return !!this.question
    }
  },

  watch: {
    question: {
      immediate: true,
      handler(newQuestion) {
        if (newQuestion) {
          this.formData = {
            text: newQuestion.text,
            question_type: newQuestion.questionType,
            is_required: newQuestion.isRequired,
            order: newQuestion.order,
            options: newQuestion.options.map(opt => ({
              text: opt.text,
              order: opt.order
            }))
          }
        } else {
          this.resetForm()
        }
      }
    },

    'formData.question_type'(newType) {
      if (newType === 'closed' && this.formData.options.length === 0) {
        this.addOption()
        this.addOption()
      } else if (newType === 'open') {
        this.formData.options = []
      }
    }
  },

  methods: {
    addOption() {
      this.formData.options.push({
        text: '',
        order: this.formData.options.length + 1
      })
    },

    removeOption(index) {
      this.formData.options.splice(index, 1)
      // Reorder remaining options
      this.formData.options.forEach((option, idx) => {
        option.order = idx + 1
      })
    },

    resetForm() {
      this.formData = {
        text: '',
        question_type: 'open',
        is_required: true,
        order: this.nextOrder,
        options: []
      }
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    },

    save() {
      if (this.$refs.form.validate()) {
        const payload = { ...this.formData }
        
        // Clean up options for open questions
        if (payload.question_type === 'open') {
          payload.options = []
        }

        this.$emit('save', payload)
      }
    }
  }
}
</script>
