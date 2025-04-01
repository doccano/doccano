<template>
  <v-card>
    <v-card-title>Define Perspective</v-card-title>
    <v-card-text>
      <v-form ref="form">
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="newQuestion"
              label="Add a Question"
              outlined
              required
              :rules="[rules.required]"
              @keyup.enter="addQuestion"
            />
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <v-radio-group v-model="questionType.id" row>
              <v-radio label="Open Question" :value="1"></v-radio>
              <v-radio label="Closed Question" :value="2"></v-radio>
            </v-radio-group>
          </v-col>
        </v-row>

        <v-row v-if="questionType.id === 2">
          <v-col cols="12">
            <v-text-field v-model="optionGroupName" label="Option Group Name" outlined required />
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="newOption"
              label="Add an Option"
              outlined
              @keyup.enter="addOption"
            />
            <v-btn color="primary" @click="addOption">Add Option</v-btn>
          </v-col>
          <v-col cols="12">
            <v-list dense>
              <v-list-item v-for="(option, index) in optionsQuestionList" :key="index">
                <v-list-item-content>
                  <v-list-item-title>{{ option.option }}</v-list-item-title>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn icon color="red" @click="removeOption(index)">
                    <v-icon>{{ mdiDelete }}</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
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
                    <v-list-item-title
                      >{{ question.question }} ({{
                        getQuestionType(question.type)
                      }})</v-list-item-title
                    >
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
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiDelete } from '@mdi/js'
import {
  CreateQuestionCommand,
  CreateOptionsGroupCommand,
  CreateOptionsQuestionCommand
} from '~/services/application/perspective/question/questionCommand'

interface QuestionType {
  id: number
  question_type: string
}

export default Vue.extend({
  data() {
    return {
      newQuestion: '',
      questionType: { id: 1, question_type: 'Open Question' } as QuestionType,
      optionGroupName: '',
      newOption: '',
      questionsList: [] as CreateQuestionCommand[],
      optionsGroupList: [] as CreateOptionsGroupCommand[],
      optionsQuestionList: [] as CreateOptionsQuestionCommand[],
      rules: {
        required: (v: string) => !!v || 'Required'
      },
      mdiDelete
    }
  },
  computed: {
    isFormValid(): boolean {
      return this.questionsList.length > 0
    }
  },
  methods: {
    getQuestionType(type: number): string {
      const types: { [key: number]: string } = {
        1: 'Open Question',
        2: 'Closed Question'
      }
      return types[type] || 'Unknown'
    },

    addOption() {
      if (this.newOption.trim()) {
        const newOptionObject: CreateOptionsQuestionCommand = {
          option: this.newOption.trim()
        }
        this.optionsQuestionList.push(newOptionObject)
        this.newOption = ''
      }
    },
    removeOption(index: number) {
      this.optionsQuestionList.splice(index, 1)
    },
    addQuestion() {
      if (!this.newQuestion.trim() || !this.questionType) {
        return
      }

      const questionData: CreateQuestionCommand = {
        question: this.newQuestion.trim(),
        type: this.questionType.id,
        options_group: undefined,
        answers: []
      }
      let optionsGroupData: CreateOptionsGroupCommand = { name: '', options_questions: [] }

      if (this.questionType.id === 2) {
        optionsGroupData = {
          name: this.optionGroupName,
          options_questions: this.optionsQuestionList
        }
        this.optionsGroupList.push(optionsGroupData)
        this.emitUpdatedOptionsGroup()
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
    emitUpdatedOptionsGroup() {
      this.$emit('update-options-group', this.optionsGroupList)
    },
    resetForm() {
      this.newQuestion = ''
      this.questionType = { id: 1, question_type: 'Open Question' }
      this.optionGroupName = ''
      this.newOption = ''
      this.optionsGroupList = []
      this.optionsQuestionList = []
    }
  }
})
</script>
