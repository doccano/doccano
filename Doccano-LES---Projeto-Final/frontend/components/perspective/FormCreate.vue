<template>
  <div>
    <v-alert v-if="errorMessage" type="error" dismissible @input="errorMessage = ''">{{ errorMessage }}</v-alert>
    <v-card>
      <v-card-title>Create Perspective</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="name" label="Add a Name" outlined required :rules="[rules.required]"/>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="newQuestion" label="Add a Question" outlined
                @keyup.enter="addQuestion" />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-radio-group v-model="questionType.id" row>
                <v-radio label="Text" :value="1"></v-radio>
                <v-radio label="Numeric" :value="2"></v-radio>
                <v-radio label="True/False" :value="3"></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-btn color="primary" @click="addQuestion">Add Question</v-btn>
            </v-col>
          </v-row>

          <v-row v-if="questionsList.length">
            <v-col cols="12">
              <v-list dense>
                <v-list-item-group>
                  <v-list-item v-for="(question, index) in questionsList" :key="index">
                    <v-list-item-content>
                      <v-list-item-title>{{ question.question }} ({{
                        getQuestionType(question.type)
                      }})</v-list-item-title>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-btn icon color="red" @click="removeQuestion(index)">
                        <v-icon>{{ mdiDelete }}</v-icon>
                      </v-btn>
                    </v-list-item-action>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <slot :valid="isFormValid" :questionsList="questionsList" />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiDelete } from '@mdi/js'
import {
  CreateQuestionCommand
} from '~/services/application/perspective/question/questionCommand'

interface QuestionType {
  id: number
  question_type: string
}

export default Vue.extend({
  data() {
    return {
      name:'',
      newQuestion: '',
      questionType: { id: 1, question_type: 'Text' } as QuestionType,
      rules: {
        required: (v: string) => !!v || 'Required',
      },
      questionsList: [] as CreateQuestionCommand[],
      errorMessage: '',
      mdiDelete
    }
  },
  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    isFormValid(): boolean {
      return this.name.trim() !== '' && this.questionsList.length > 0
    },
  },

  watch: {
    // Emitir mudanças no nome da perspectiva
    name(newName) {
      this.$emit('update-name', newName)
    }
  },
  methods: {

    getQuestionType(type: number): string {
      const types: { [key: number]: string } = {
        1: 'Text',
        2: 'Numeric',
        3: 'True/False'
      }
      return types[type] || 'Unknown'
    },

    addQuestion() {
      this.errorMessage = ''
      if (!this.newQuestion.trim()) {
        this.errorMessage = "The question cannot be empty"
        return
      }
      const questionData: CreateQuestionCommand = {
        question: this.newQuestion.trim(),
        type: this.questionType.id,
        options_group: undefined,
        answers: []
      }

      this.questionsList.push(questionData)
      this.emitUpdatedQuestions()
      this.resetForm()
    },
    removeQuestion(index: number) {
      this.questionsList.splice(index, 1)
      this.emitUpdatedQuestions()
    },
    emitUpdatedQuestions() {
      this.$emit('update-questions', this.questionsList)
    },
    resetForm() {
      this.newQuestion = ''
      this.questionType = { id: 1, question_type: 'Text' }
    }
  },
})
</script>
