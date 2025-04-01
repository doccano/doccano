<template>
  <div>
    <v-alert v-if="sucessMessage" type="success" dismissible>{{ sucessMessage }}</v-alert>
    <v-alert v-if="errorMessage" type="error" dismissible>{{ errorMessage }}</v-alert>
    <form-create
      v-slot="slotProps"
      v-bind.sync="editedItem"
      :perspective-id="null"
      :items="items"
      @update-questions="updateQuestions"
      @update-options-group="updateOptionsGroup"
    >
      <v-btn color="error" class="text-capitalize" @click="$router.back()"> Cancel </v-btn>
      <v-btn :disabled="!slotProps.valid" color="primary" class="text-capitalize" @click="save">
        Save
      </v-btn>
    </form-create>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import FormCreate from '~/components/perspective/FormCreate.vue'
import { CreatePerspectiveCommand } from '~/services/application/perspective/perspectiveCommand'
import { PerspectiveDTO } from '~/services/application/perspective/perspectiveData'
import { CreateOptionsGroupCommand } from '~/services/application/perspective/question/questionCommand'
import {
  OptionsGroupDTO,
  QuestionDTO,
  QuestionTypeDTO
} from '~/services/application/perspective/question/questionData'

export default Vue.extend({
  components: {
    FormCreate
  },

  layout: 'projects',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      editedItem: {
        id: null,
        project_id: 0,
        questions: [],
        members: []
      } as CreatePerspectiveCommand,

      optionsGroupItem: [
        {
          name: '',
          options_questions: []
        }
      ] as CreateOptionsGroupCommand[],

      questionTypeItem: [
        {
          id: 1,
          question_type: 'Open Question'
        },
        {
          id: 2,
          question_type: 'Closed Question'
        }
      ] as QuestionTypeDTO[],

      defaultItem: {
        id: null,
        project_id: 0,
        questions: [],
        members: []
      } as CreatePerspectiveCommand,

      errorMessage: '',
      sucessMessage: '',
      items: [] as PerspectiveDTO[]
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    service(): any {
      return this.$services.perspective
    }
  },

  methods: {
    updateQuestions(questions: QuestionDTO[]) {
      this.editedItem.questions = questions
    },

    updateOptionsGroup(optionsGroup: OptionsGroupDTO[]) {
      this.optionsGroupItem = optionsGroup
      console.log(this.optionsGroupItem)
    },

    async save() {
      try {
        this.editedItem.project_id = Number(this.projectId)
        this.editedItem.members = await this.getAnnotatorIds()
        let j = 0
        const questionTypeOpen = await this.$services.questionType.findById(
          this.projectId,
          this.questionTypeItem[0].id
        )
        const questionTypeClosed = await this.$services.questionType.findById(
          this.projectId,
          this.questionTypeItem[1].id
        )
        if (!questionTypeOpen || !questionTypeOpen.id)
          await this.$services.questionType.create(this.projectId, {
            id: this.questionTypeItem[0].id,
            question_type: this.questionTypeItem[0].question_type
          })
        if (!questionTypeClosed || !questionTypeClosed.id)
          await this.$services.questionType.create(this.projectId, {
            id: this.questionTypeItem[1].id,
            question_type: this.questionTypeItem[1].question_type
          })
        for (let i = 0; i < this.editedItem.questions.length; i++) {
          if (this.editedItem.questions[i].type === 2) {
            console.log(this.optionsGroupItem[j])
            const existingOptionGroup = await this.$services.optionsGroup.findByName(
              this.projectId,
              this.optionsGroupItem[j].name
            )

            if (existingOptionGroup && existingOptionGroup.id) {
              this.editedItem.questions[i].options_group = existingOptionGroup.id
            } else {
              const optionGroup = await this.$services.optionsGroup.create(
                this.projectId,
                this.optionsGroupItem[j]
              )
              this.editedItem.questions[i].options_group = optionGroup.id
            }
            j++
          }
        }
        await this.service.create(this.projectId, this.editedItem)
        this.sucessMessage = 'A perspective has been successfully added to this project'
        setTimeout(() => {
          this.$router.push(`/projects/${this.projectId}/perspectives`)
        }, 1000)
      } catch (error) {
        this.handleError(error)
      }
    },
    async getAnnotatorIds(): Promise<number[]> {
      const members = await this.$repositories.member.list(this.projectId)
      return members.filter((member) => member.rolename === 'annotator').map((member) => member.id)
    },
    handleError(error: any) {
      this.editedItem = Object.assign({}, this.defaultItem)
      if (error.response && error.response.status === 400) {
        this.errorMessage = 'This project already has a perspective linked to it.'
      } else {
        this.errorMessage = 'Database is slow or unavailable. Please try again later.'
      }
    }
  }
})
</script>
