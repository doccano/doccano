<template>
  <div class="perspectives-container">
    <!-- Alertas com design melhorado -->
    <v-slide-y-transition>
      <v-alert
        v-if="successMessage"
        type="success"
        dismissible
        border="left"
        colored-border
        elevation="2"
        class="ma-4"
        @click="successMessage = ''"
      >
        <v-icon slot="prepend" color="success">mdi-check-circle</v-icon>
        {{ successMessage }}
      </v-alert>
    </v-slide-y-transition>

    <v-slide-y-transition>
      <v-alert
        v-if="errorMessage"
        type="error"
        dismissible
        border="left"
        colored-border
        elevation="2"
        class="ma-4"
        @click="errorMessage = ''"
      >
        <v-icon slot="prepend" color="error">mdi-alert-circle</v-icon>
        {{ errorMessage }}
      </v-alert>
    </v-slide-y-transition>

    <v-slide-y-transition>
      <v-alert
        v-if="databaseError"
        type="warning"
        dismissible
        border="left"
        colored-border
        elevation="2"
        class="ma-4"
        @click="databaseError = ''"
      >
        <v-icon slot="prepend" color="warning">mdi-database-alert</v-icon>
        {{ databaseError }}
      </v-alert>
    </v-slide-y-transition>

    <!-- Card principal com design melhorado -->
    <v-card class="main-card" elevation="3">
      <template v-if="isAnswered">
        <v-card-title class="primary white--text d-flex align-center">
          <v-icon left color="white" size="28">mdi-check-circle-outline</v-icon>
          <span class="text-h5">Perspectiva Pessoal Já Definida</span>
        </v-card-title>
        <v-card-text class="pa-6 text-center">
          <v-icon size="80" color="success" class="mb-4">mdi-account-check</v-icon>
          <p class="text-h6 mb-0">A sua perspectiva pessoal já foi submetida para este projeto.</p>
        </v-card-text>
      </template>

      <template v-else>
        <template v-if="isAdmin">
          <!-- Seção de Administração -->
          <v-card-title class="primary white--text d-flex align-center">
            <v-icon left color="white" size="28">mdi-cog</v-icon>
            <span class="text-h5">Gestão de Perspectivas</span>
          </v-card-title>
          
          <v-card-text class="pa-0">
            <!-- Barra de ações com design melhorado -->
            <v-toolbar flat color="grey lighten-4" class="px-4">
              <action-menu 
                :disabled="hasPerspectives" 
                @create="$router.push('perspectives/add')"
              />
              <v-spacer></v-spacer>
              <v-btn 
                :disabled="selected.length === 0"
                class="text-capitalize" 
                outlined 
                color="error"
                @click.stop="dialogDelete = true"
              >
                <v-icon left>mdi-delete</v-icon>
                {{ $t('generic.delete') }}
              </v-btn>
            </v-toolbar>

            <!-- Lista de perspectivas -->
            <div class="pa-4">
              <perspective-list 
                v-model="selected" 
                :items="items" 
                :is-loading="isLoading" 
              />
            </div>
          </v-card-text>

          <!-- Dialog de confirmação de exclusão -->
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="error white--text">
                <v-icon left color="white">mdi-delete-alert</v-icon>
                Confirmar Exclusão
              </v-card-title>
              <v-card-text class="pa-4">
                <p class="mb-0">Tem certeza que deseja excluir os itens selecionados?</p>
              </v-card-text>
              <v-card-actions class="pa-4">
                <v-spacer></v-spacer>
                <v-btn text @click="dialogDelete = false">Cancelar</v-btn>
                <v-btn color="error" @click="handleDelete">Excluir</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </template>

        <template v-else>
          <!-- Seção do Utilizador -->
          <v-card-title class="primary white--text d-flex align-center">
            <v-icon left color="white" size="28">mdi-account-question</v-icon>
            <span class="text-h5">Definir Perspectiva Pessoal</span>
          </v-card-title>
          
          <v-card-text class="pa-6">
            <form-answer
              :questions-list="questionsList"
              :options-list="optionsList"
              :project-id="projectId"
              @submit-answers="submitAnswers"
            />
          </v-card-text>
        </template>
      </template>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import ActionMenu from '@/components/perspective/ActionMenu.vue'
import PerspectiveList from '@/components/perspective/PerspectiveList.vue'
import FormAnswer from '~/components/perspective/FormAnswer.vue'
import {
  AnswerItem,
  CreateAnswerCommand,
  MemberItem,
  PerspectiveDTO,
  QuestionItem
} from '~/domain/models/perspective/perspectiveItem'
import { OptionsQuestionItem } from '~/domain/models/perspective/question/question'

export default Vue.extend({
  components: {
    ActionMenu,
    PerspectiveList,
    FormAnswer
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      dialogDelete: false,
      items: [] as PerspectiveDTO[],
      selected: [] as PerspectiveDTO[],
      isLoading: false,
      tab: 0,
      drawerLeft: null,
      myRole: null as MemberItem | null,
      questionsList: [] as QuestionItem[],
      answersList: [] as AnswerItem[],
      optionsList: [] as OptionsQuestionItem[],
      AlreadyAnswered: false,
      submitted: false,
      successMessage: '',
      errorMessage: '',
      databaseError: '',
      databaseCheckInterval: null as NodeJS.Timeout | null
    }
  },

  computed: {
    ...mapGetters('auth', ['isStaff', 'isSuperUser']),
    projectId(): string {
      return this.$route.params.id
    },
    isAdmin(): boolean {
      return this.myRole?.isProjectAdmin ?? false
    },
    isSubmitted(): boolean {
      return this.submitted
    },
    isAnswered(): boolean {
      return this.AlreadyAnswered
    },
    hasPerspectives(): boolean {
      return this.items.length > 0
    }
  },

  async mounted() {
    try {
      const memberRepository = this.$repositories.member
      this.myRole = await memberRepository.fetchMyRole(this.projectId)
      if (this.isAdmin) {
        await this.fetchPerspectives()
      } else {
        await this.fetchQuestions()
        await this.fetchAnswers()
        await this.fetchOptions()
      }
      
      // Iniciar verificação da database de 1 em 1 segundo
      this.startDatabaseCheck()
    } catch (error) {
      console.error('Erro ao buscar o papel ou perguntas:', error)
    }
  },

  beforeDestroy() {
    // Limpar o intervalo quando o componente for destruído
    if (this.databaseCheckInterval) {
      clearInterval(this.databaseCheckInterval)
    }
  },

  methods: {
    startDatabaseCheck() {
      this.databaseCheckInterval = setInterval(async () => {
        try {
          // Fazer uma chamada simples para verificar se a database está disponível
          await this.$services.perspective.list(this.projectId)
          // Se chegou até aqui, a database está funcionando
          if (this.databaseError) {
            this.databaseError = ''
          }
        } catch (error: any) {
          console.error('Erro na verificação da database:', error)
          if (error.response && error.response.status >= 500) {
            this.databaseError = 'Base de dados indisponível. Tentando reconectar...'
          } else if (error.code === 'NETWORK_ERROR' || !error.response) {
            this.databaseError = 'Erro de conexão com a base de dados. Verificando conectividade...'
          }
        }
      }, 1000) // 1 segundo
    },

    async fetchPerspectives() {
      this.isLoading = true
      try {
        const projectId = this.$route.params.id
        const response = await this.$services.perspective.list(projectId)
        this.items = response
      } catch (error) {
        console.error('Erro ao buscar perspectivas:', error)
        this.items = []
      } finally {
        this.isLoading = false
      }
    },

    async fetchAnswers() {
      this.isLoading = true
      try {
        const response = await this.$services.answer.list()
        console.log('Respostas:', response)
        this.AlreadyAnswered = response.some((answer: AnswerItem) => {
          return this.questionsList.some((question) => question.id === answer.question) &&
                 answer.member === this.myRole?.id;
        });
        console.log('Respondeu?', this.AlreadyAnswered)
      } catch (error) {
        console.error('Erro ao buscar respostas:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchQuestions() {
      this.isLoading = true
      try {
        // Obtém as perspectivas do projeto
        const perspectives = await this.$services.perspective.list(this.projectId)
        if (perspectives.length > 0) {
          const perspectiveId = perspectives[0].id
          const questions = await this.$services.question.list(perspectiveId, this.projectId)
          this.questionsList = questions.filter((question) => question.perspective_id === perspectiveId)
          console.log('Perguntas:', this.questionsList)
        } else {
          this.questionsList = []
        }
      } catch (error) {
        console.error('Erro ao buscar perguntas:', error)
        this.questionsList = []
      } finally {
        this.isLoading = false
      }
    },

    async fetchOptions() {
      this.isLoading = true
      try {
        const response = await this.$services.optionsQuestion.list(this.projectId)
        this.optionsList = response
        console.log('Opções:', this.optionsList)
      } catch (error) {
        console.error('Erro ao buscar opções:', error)
      } finally {
        this.isLoading = false
      }
    },

    async handleDelete() {
      this.isLoading = true
      try {
        for (const user of this.selected) {
          await this.$services.user.delete(user.id)
        }
        this.items = this.items.filter(
          (user) => !this.selected.some((selectedUser) => selectedUser.id === user.id)
        )
        this.selected = []
        this.dialogDelete = false
      } catch (error) {
        console.error('Erro ao excluir perspectivas:', error)
      } finally {
        this.isLoading = false
      }
    },

    async submitAnswers(formattedAnswers: { questionId: number; answer: string; questionType: number }[], projectId: string) {
      console.log('Respostas submetidas:', formattedAnswers)
      try {
        // Todas as respostas agora são do tipo texto (Text, Numeric, True/False)
        const answersToSubmit: CreateAnswerCommand[] = formattedAnswers.map((formattedAnswer) => {
          return {
            member: this.myRole?.id || 0,
            question: formattedAnswer.questionId,
            answer_text: formattedAnswer.answer
          }
        })

        for (const answer of answersToSubmit) {
          await this.$services.answer.create(projectId, answer)
        }
        this.successMessage = 'Answers successfully submitted!'
        setTimeout(() => {
          this.successMessage = ''
          this.submitted = true
          this.$router.push(`/projects/${this.projectId}/perspectives`)
        }, 7000)
        window.location.reload();
      } catch (error: any) {
        console.error('Erro ao submeter respostas:', error)
        if (error.response && error.response.status === 400) {
          const errors = error.response.data
          if (errors.answer_text) {
            this.errorMessage = errors.answer_text[0]
          } else {
            this.errorMessage = JSON.stringify(errors)
          }
        } else if (error.response && error.response.status === 500) {
          this.errorMessage = 'Database is slow or unavailable. Please try again later.'
        } else {
          this.errorMessage = 'Database is slow or unavailable. Please try again later.'
        }
      }
    }
  }
})
</script>

<style scoped>
.perspectives-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px;
}

.main-card {
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 16px !important;
  overflow: hidden;
}

.v-card-title {
  border-radius: 0 !important;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.v-alert {
  border-radius: 12px !important;
  font-weight: 500;
}

.v-toolbar {
  border-radius: 0 !important;
}

.v-btn {
  border-radius: 8px !important;
  font-weight: 600;
  text-transform: none !important;
}

.v-dialog .v-card {
  border-radius: 16px !important;
}

/* Transições suaves */
.v-slide-y-transition-enter-active,
.v-slide-y-transition-leave-active {
  transition: all 0.3s ease;
}

.v-slide-y-transition-enter,
.v-slide-y-transition-leave-to {
  transform: translateY(-15px);
  opacity: 0;
}
</style>
