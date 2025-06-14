<template>
  <div class="perspective-list-container">
    <!-- Card de filtros com design melhorado -->
    <v-card class="filters-card mb-4" elevation="2">
      <v-card-title class="pb-2">
        <v-icon left color="primary">mdi-filter-variant</v-icon>
        <span class="text-h6">Filtros</span>
        <v-spacer></v-spacer>
        <v-btn 
          :disabled="!hasActiveFilters"
          color="secondary" 
          text
          small 
          class="clear-filters-btn"
          @click="clearAllFilters"
        >
          <v-icon left small>mdi-filter-remove</v-icon>
          Limpar Filtros
        </v-btn>
      </v-card-title>
      
      <v-card-text class="pt-0">
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              v-model="selectedQuestion"
              :items="availableQuestions"
              label="Selecione a pergunta"
              clearable
              outlined
              dense
              prepend-icon="mdi-help-circle-outline"
              class="filter-select"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="selectedUser"
              :items="availableUsers"
              label="Selecione o utilizador"
              clearable
              outlined
              dense
              prepend-icon="mdi-account-outline"
              class="filter-select"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="selectedAnswer"
              :items="availableAnswers"
              label="Selecione a resposta"
              clearable
              outlined
              dense
              prepend-icon="mdi-comment-text-outline"
              class="filter-select"
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Card da tabela com design melhorado -->
    <v-card class="data-table-card" elevation="2">
      <v-card-title class="pb-2">
        <v-icon left color="primary">mdi-table</v-icon>
        <span class="text-h6">Respostas das Perspectivas</span>
        <v-spacer></v-spacer>
        <v-chip 
          v-if="processedItems.length > 0" 
          color="primary" 
          text-color="white" 
          small
        >
          {{ processedItems.length }} {{ processedItems.length === 1 ? 'resultado' : 'resultados' }}
        </v-chip>
      </v-card-title>

      <v-card-text class="pt-0">
        <!-- Campo de busca melhorado -->
        <v-text-field
          v-model="search"
          :prepend-inner-icon="mdiMagnify"
          :label="$t('generic.search')"
          single-line
          hide-details
          filled
          clearable
          class="mb-4 search-field"
          background-color="grey lighten-5"
        />

        <!-- Tabela de dados melhorada -->
        <v-data-table
          :items="processedItems"
          :headers="headers"
          :loading="isLoading"
          :loading-text="$t('generic.loading')"
          :no-data-text="$t('vuetify.noDataAvailable')"
          :footer-props="{
            showFirstLastPage: true,
            'items-per-page-text': $t('vuetify.itemsPerPageText'),
            'page-text': $t('dataset.pageText')
          }"
          item-key="id"
          show-select
          class="elevation-1 data-table"
          @input="$emit('input', $event)"
        >
          <!-- Oculta o checkbox do header -->
          <template #[`header.data-table-select`]>
            <!-- slot vazio -->
          </template>
          
          <template #[`item.memberName`]="{ item }">
            <div class="d-flex align-center">
              <v-avatar size="32" color="primary" class="mr-3">
                <v-icon color="white" size="16">mdi-account</v-icon>
              </v-avatar>
              <span class="font-weight-medium">{{ item.memberName }}</span>
            </div>
          </template>
          
          <template #[`item.question`]="{ item }">
            <div class="question-cell">
              <v-tooltip bottom>
                <template #activator="{ on, attrs }">
                  <span 
                    v-bind="attrs"
                    class="question-text"
                    v-on="on"
                  >
                    {{ item.question }}
                  </span>
                </template>
                <span>{{ item.question }}</span>
              </v-tooltip>
            </div>
          </template>
          
          <template #[`item.answer`]="{ item }">
            <v-chip
              :color="getAnswerChipColor(item.answer)"
              text-color="white"
              small
              class="font-weight-medium"
            >
              {{ item.answer }}
            </v-chip>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMagnify } from '@mdi/js'
import type { PropType } from 'vue'
import { PerspectiveDTO } from '~/services/application/perspective/perspectiveData'

export default Vue.extend({
  name: 'PerspectiveList',
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    // Os itens (perspectivas) devem já vir filtrados ou possuir um atributo project_id
    items: {
      type: Array as PropType<PerspectiveDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<PerspectiveDTO[]>,
      default: () => [],
      required: true
    },
    disableEdit: {
      type: Boolean,
      default: false
    },
    members: {
      type: Array as PropType<any[]>,
      default: () => []
    }
  },

  data() {
    return {
      search: '',
      mdiMagnify,
      // Selecção dos filtros: pergunta, utilizador e resposta
      selectedQuestion: null as string | null,
      selectedUser: null as string | null,
      selectedAnswer: null as string | null,
      // Armazena os nomes carregados para os IDs de 0 a 100
      memberNames: {} as { [key: number]: string }
    }
  },

  computed: {
    // Header com três colunas: Criador, Pergunta e Resposta
    headers() {
      return [
        { text: this.$t('Created by'), value: 'memberName', sortable: true, width: '200px' },
        { text: this.$t('Question'), value: 'question', sortable: true, width: '40%' },
        { text: this.$t('Answer'), value: 'answer', sortable: true, width: '200px' }
      ]
    },
    projectId(): string {
      return this.$route.params.id
    },
    // Extrai as perguntas disponíveis e adiciona a opção "Todas as perguntas"
    availableQuestions() {
      const questionsSet = new Set<string>()
      const projectItems = this.items.filter(
        item => Number(item.project_id) === Number(this.projectId)
      )
      projectItems.forEach(item => {
        if (Array.isArray(item.questions)) {
          item.questions.forEach(q => {
            if (q.question) {
              questionsSet.add(q.question)
            }
          })
        }
      })
      return Array.from(questionsSet)
    },
    // Extrai os utilizadores disponíveis a partir das respostas e adiciona "Todos os utilizadores"
    availableUsers() {
      const usersSet = new Set<string>()
      const projectItems = this.items.filter(
        item => Number(item.project_id) === Number(this.projectId)
      )
      projectItems.forEach(item => {
        if (Array.isArray(item.questions)) {
          item.questions.forEach(q => {
            if (Array.isArray(q.answers)) {
              q.answers.forEach((a: any) => {
                let memberName = ''
                if (a.member) {
                  if (typeof a.member === 'object' && a.member.name) {
                    memberName = a.member.name
                  } else if (typeof a.member === 'number') {
                    memberName = this.memberNames[a.member] || a.member.toString()
                  }
                  if (memberName) {
                    usersSet.add(memberName)
                  }
                }
              })
            }
          })
        }
      })
      return Array.from(usersSet)
    },
    // Extrai as respostas disponíveis e adiciona "Todas as respostas"
    availableAnswers() {
      const answersSet = new Set<string>()
      const projectItems = this.items.filter(
        item => Number(item.project_id) === Number(this.projectId)
      )
      projectItems.forEach(item => {
        if (Array.isArray(item.questions)) {
          item.questions.forEach(q => {
            if (Array.isArray(q.answers)) {
              q.answers.forEach((a: any) => {
                const answerText = a.answer_text || a.answer_option || ''
                if (answerText) {
                  answersSet.add(answerText)
                }
              })
            }
          })
        }
      })
      return Array.from(answersSet)
    },
    // Processa os itens gerando uma linha para cada resposta e aplicando os filtros selecionados
    processedItems() {
      const result: Array<{ id: number; memberName: string; question: string; answer: string }> = []
      const projectItems = this.items.filter(
        item => Number(item.project_id) === Number(this.projectId)
      )
      let counter = 0
      projectItems.forEach(item => {
        if (Array.isArray(item.questions)) {
          item.questions.forEach(q => {
            // Filtra pela pergunta, se selecionada
            if (this.selectedQuestion && 
                q.question && q.question.toLowerCase() !== this.selectedQuestion.toLowerCase()) {
              return
            }
            if (Array.isArray(q.answers)) {
              q.answers.forEach((a: any) => {
                let memberId: number 
                let memberName = ''
                if (a.member) {
                  if (typeof a.member === 'object' && a.member.id != null) {
                    memberId = a.member.id
                    memberName = a.member.name || memberId.toString()
                  } else if (typeof a.member === 'number') {
                    memberId = a.member
                    memberName = this.memberNames[memberId] || memberId.toString()
                  }
                }
                const answerText = a.answer_text || a.answer_option || ''
                // Cria um registro para cada resposta
                const row = {
                  id: counter++,
                  memberName,
                  question: q.question,
                  answer: answerText
                }
                // Filtro de busca (buscando em todas as colunas)
                if (this.search) {
                  const searchLower = this.search.toLowerCase()
                  const combinedText = `${row.memberName} ${row.question} ${row.answer}`.toLowerCase()
                  if (!combinedText.includes(searchLower)) {
                    return
                  }
                }
                // Filtro por utilizador, se selecionado
                if (this.selectedUser &&
                    row.memberName.toLowerCase() !== this.selectedUser.toLowerCase()) {
                  return
                }
                // Filtro por resposta, se selecionada
                if (this.selectedAnswer &&
                    row.answer.toLowerCase() !== this.selectedAnswer.toLowerCase()) {
                  return
                }
                result.push(row)
              })
            }
          })
        }
      })
      return result
    },
    hasActiveFilters() {
      return this.selectedQuestion !== null || this.selectedUser !== null || this.selectedAnswer !== null || this.search !== ''
    }
  },

  watch: {
    selectedQuestion(newVal) {
      console.log('selectedQuestion changed:', newVal)
    },
    selectedUser(newVal) {
      console.log('selectedUser changed:', newVal)
    },
    selectedAnswer(newVal) {
      console.log('selectedAnswer changed:', newVal)
    },
    // Quando os itens mudam, recarrega os nomes dos membros
    items: {
      handler() {
        this.$nextTick(() => {
          this.loadMemberNames()
        })
      },
      deep: true,
      immediate: true
    }
  },

  mounted() {
    this.$nextTick(() => {
      this.loadMemberNames()
    })
  },

  methods: {
    // Exemplo de método para carregar os nomes dos membros (supondo um repositório para membros)
    loadMemberNames() {
      for (let memberId = 0; memberId <= 100; memberId++) {
        this.$repositories.member.findById(this.projectId, memberId)
          .then((response: any) => {
            this.$set(this.memberNames, memberId, response.username)
            console.log(`Fetched member ${memberId}:`, response.username)
          })
          .catch(() => {
            console.log(`Member not found for ID ${memberId}`)
          })
      }
    },
    clearAllFilters() {
      this.selectedQuestion = null
      this.selectedUser = null
      this.selectedAnswer = null
      this.search = ''
    },
    getAnswerChipColor(answer: string) {
      // Retorna cores diferentes baseadas no tipo de resposta
      if (!answer) return 'grey'
      
      // Para respostas True/False
      if (answer.toLowerCase() === 'true' || answer.toLowerCase() === 'sim') return 'success'
      if (answer.toLowerCase() === 'false' || answer.toLowerCase() === 'não') return 'error'
      
      // Para respostas numéricas
      if (!isNaN(Number(answer))) {
        const num = Number(answer)
        if (num > 7) return 'success'
        if (num > 4) return 'warning'
        return 'error'
      }
      
      // Para outras respostas
      return 'primary'
    }
  }
})
</script>

<style scoped>
.perspective-list-container {
  padding: 0;
}

.filters-card {
  border-radius: 12px !important;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
}

.data-table-card {
  border-radius: 12px !important;
  background: #ffffff;
}

.filter-select {
  border-radius: 8px;
}

.clear-filters-btn {
  border-radius: 20px !important;
  text-transform: none !important;
  font-weight: 600;
}

.search-field {
  border-radius: 12px !important;
}

.data-table {
  border-radius: 8px !important;
}

.question-cell {
  max-width: 300px;
}

.question-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
  cursor: help;
}

.v-chip {
  border-radius: 16px !important;
}

.v-card-title {
  font-weight: 600;
  color: #424242;
}

.v-data-table ::v-deep .v-data-table__wrapper {
  border-radius: 8px;
}

.v-data-table ::v-deep th {
  background-color: #f5f5f5 !important;
  font-weight: 600 !important;
  color: #424242 !important;
}

.v-data-table ::v-deep tbody tr:hover {
  background-color: rgba(25, 118, 210, 0.04) !important;
}

/* Animações suaves */
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
}

.v-chip {
  transition: all 0.2s ease;
}

.v-chip:hover {
  transform: scale(1.05);
}
</style>