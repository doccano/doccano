<template>
  <div>
    <v-alert v-if="sucessMessage" type="success" dismissible>{{ sucessMessage }}</v-alert>
    <v-alert v-if="errorMessage" type="error" dismissible>{{ errorMessage }}</v-alert>
    <v-alert v-if="databaseError" type="error" persistent class="mb-4">
      Database unavailable. Please try again later.
    </v-alert>
    <form-create
      v-bind.sync="editedItem"
      :perspective-id="null"
      :items="items"
      :disabled="databaseError"
      @update-questions="updateQuestions"
      @update-name="updateName"
    >
      <v-btn color="error" class="text-capitalize" @click="$router.back()"> Cancel </v-btn>
      <v-btn 
        :disabled="!isFormValid || databaseError" 
        color="primary" 
        class="text-capitalize" 
        @click="save"
      >
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
import {
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
        name: '',
        project_id: 0,
        questions: [],
        members: []
      } as CreatePerspectiveCommand,

      questionTypeItem: [
        {
          id: 1,
          question_type: 'Text'
        },
        {
          id: 2,
          question_type: 'Numeric'
        },
        {
          id: 3,
          question_type: 'True/False'
        }
      ] as QuestionTypeDTO[],

      defaultItem: {
        id: null,
        name: '',
        project_id: 0,
        questions: [],
        members: []
      } as CreatePerspectiveCommand,

      errorMessage: '',
      sucessMessage: '',
      items: [] as PerspectiveDTO[],
      databaseError: false,
      connectionCheckInterval: null as any,
      perspectiveName: ''
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    service(): any {
      return this.$services.perspective
    },

    // Validação completa do formulário
    isFormValid(): boolean {
      return this.perspectiveName.trim() !== '' && this.editedItem.questions.length > 0
    }
  },

  mounted() {
    // Iniciar verificação da conexão quando o componente for montado
    this.startConnectionCheck()
  },

  beforeDestroy() {
    // Parar verificação quando o componente for destruído
    this.stopConnectionCheck()
  },

  methods: {
    updateQuestions(questions: QuestionDTO[]) {
      this.editedItem.questions = questions
    },

    updateName(name: string) {
      this.perspectiveName = name
    },

    // Verifica a conexão com a base de dados
    async checkDatabaseConnection() {
      try {
        // Faz uma chamada simples para testar a conexão
        await this.$repositories.member.fetchMyRole(this.projectId)
        this.databaseError = false
      } catch (error) {
        console.error('Erro de conexão com a base de dados:', error)
        this.databaseError = true
      }
    },

    // Inicia a verificação periódica da conexão
    startConnectionCheck() {
      // Verificação inicial
      this.checkDatabaseConnection()
      
      // Configurar verificação a cada 2 segundos
      this.connectionCheckInterval = setInterval(() => {
        this.checkDatabaseConnection()
      }, 2000)
    },

    // Para a verificação periódica
    stopConnectionCheck() {
      if (this.connectionCheckInterval) {
        clearInterval(this.connectionCheckInterval)
        this.connectionCheckInterval = null
      }
    },

    async save() {
      // Verificar se a base de dados está disponível antes de tentar salvar
      if (this.databaseError) {
        this.errorMessage = 'Database unavailable. Please try again later.'
        return
      }

      try {
        this.editedItem.project_id = Number(this.projectId)
        this.editedItem.name = this.perspectiveName.trim()
        this.editedItem.members = await this.getAnnotatorIds();
        
        // Garantir que os tipos de pergunta existem
        const questionTypeText = await this.$services.questionType.findById(
          this.projectId,
          this.questionTypeItem[0].id
        )
        const questionTypeNumeric = await this.$services.questionType.findById(
          this.projectId,
          this.questionTypeItem[1].id
        )
        const questionTypeTrueFalse = await this.$services.questionType.findById(
          this.projectId,
          this.questionTypeItem[2].id
        )
        
        if (!questionTypeText || !questionTypeText.id)
          await this.$services.questionType.create(this.projectId, {
            id: this.questionTypeItem[0].id,
            question_type: this.questionTypeItem[0].question_type
          })
        if (!questionTypeNumeric || !questionTypeNumeric.id)
          await this.$services.questionType.create(this.projectId, {
            id: this.questionTypeItem[1].id,
            question_type: this.questionTypeItem[1].question_type
          })
        if (!questionTypeTrueFalse || !questionTypeTrueFalse.id)
          await this.$services.questionType.create(this.projectId, {
            id: this.questionTypeItem[2].id,
            question_type: this.questionTypeItem[2].question_type
          })
        
        await this.service.create(this.projectId, this.editedItem)
        this.sucessMessage = 'A perspective has been successfully added to this project and an email has been sent to all annotators of the project'
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
      
      // Detectar erros de conexão com a base de dados
      if (error.response && error.response.status === 503) {
        this.databaseError = true
        this.errorMessage = ''
      } else if (error.response && error.response.status === 400) {
        const errorData = error.response.data
        
        // Verificar se é erro de nome duplicado
        if (errorData && errorData.name && errorData.name[0]) {
          this.errorMessage = errorData.name[0]
        } else if (errorData && errorData.error) {
          this.errorMessage = errorData.error
        } else {
          this.errorMessage = 'Já existe uma perspectiva com esse nome.'
        }
        this.databaseError = false
      } else if (error.code === 'NETWORK_ERROR' || error.message.includes('Network Error')) {
        this.databaseError = true
        this.errorMessage = ''
      } else {
        this.errorMessage = 'Database is slow or unavailable. Please try again later.'
        this.databaseError = false
      }
    }
  }
})
</script>
