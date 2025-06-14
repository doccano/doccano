<template>
  <div class="form-answer-container">
    <!-- Card de estado vazio -->
    <v-card v-if="questionsList.length == 0" class="empty-state-card" elevation="2">
      <v-card-text class="text-center pa-8">
        <v-icon size="80" color="grey lighten-1" class="mb-4">mdi-help-circle-outline</v-icon>
        <h3 class="text-h5 grey--text text--darken-1 mb-2">Nenhuma Pergunta Encontrada</h3>
        <p class="text-body-1 grey--text">Não foram encontradas questões na perspectiva para este projeto.</p>
      </v-card-text>
    </v-card>

    <!-- Formulário principal -->
    <div v-else class="questions-container">
      <v-form ref="form">
        <!-- Progresso do formulário -->
        <v-card class="progress-card mb-4" elevation="1">
          <v-card-text class="pa-4">
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-body-2 font-weight-medium">Progresso do Formulário</span>
              <span class="text-caption">{{ answeredQuestions }}/{{ questionsList.length }}</span>
            </div>
            <v-progress-linear
              :value="progressPercentage"
              height="8"
              rounded
              color="primary"
              background-color="grey lighten-3"
            ></v-progress-linear>
          </v-card-text>
        </v-card>

        <!-- Lista de perguntas -->
        <div class="questions-list">
          <v-card 
            v-for="(question, index) in questionsList" 
            :key="question.id" 
            class="question-card mb-4" 
            elevation="2"
          >
            <v-card-title class="question-header">
              <div class="question-number">
                <v-avatar size="32" color="primary">
                  <span class="white--text font-weight-bold">{{ index + 1 }}</span>
                </v-avatar>
              </div>
              <div class="question-title ml-3">
                <h4 class="text-h6 mb-0">{{ question.question }}</h4>
              </div>
            </v-card-title>

            <v-card-text class="pt-2">
              <!-- Perguntas com opções (múltipla escolha) -->
              <div v-if="question.options_group !== null" class="options-container">
                <v-radio-group 
                  v-model="answers[question.id]" 
                  class="custom-radio-group"
                >
                  <v-radio
                    v-for="option in getOptionsForQuestion(question.options_group)"
                    :key="option.id"
                    :label="option.option"
                    :value="option.id"
                    class="custom-radio mb-2"
                    color="primary"
                  />
                </v-radio-group>
              </div>

              <!-- Perguntas de texto livre -->
              <div v-else class="text-input-container">
                <v-text-field
                  v-model="answers[question.id]"
                  label="Digite a sua resposta"
                  outlined
                  dense
                  clearable
                  class="custom-text-field"
                  :rules="[v => !!v || 'Este campo é obrigatório']"
                  prepend-inner-icon="mdi-pencil-outline"
                />
              </div>
            </v-card-text>
          </v-card>
        </div>

        <!-- Botões de ação -->
        <v-card class="actions-card mt-6" elevation="2">
          <v-card-text class="pa-4">
            <div class="d-flex justify-space-between align-center">
                             <v-btn
                 color="warning"
                 outlined
                 large
                 class="action-btn"
                 @click="clearAnswers"
               >
                <v-icon left>mdi-refresh</v-icon>
                Limpar Respostas
              </v-btn>

                             <v-btn
                 :disabled="!isFormValid"
                 color="primary"
                 large
                 elevated
                 class="action-btn submit-btn"
                 @click="openConfirmDialog"
               >
                <v-icon left>mdi-check-circle</v-icon>
                Submeter Respostas
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-form>
    </div>

    <!-- Diálogo de confirmação melhorado -->
    <v-dialog v-model="confirmDialog" persistent max-width="500px">
      <v-card class="confirmation-dialog" elevation="8">
        <v-card-title class="primary white--text">
          <v-icon left color="white">mdi-help-circle</v-icon>
          Confirmar Submissão
        </v-card-title>
        
        <v-card-text class="pa-6">
          <div class="text-center">
            <v-icon size="60" color="primary" class="mb-4">mdi-file-document-check</v-icon>
            <p class="text-h6 mb-2">Tem certeza que deseja submeter as respostas?</p>
            <p class="text-body-2 grey--text">Esta ação não pode ser desfeita.</p>
          </div>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn text color="grey" @click="handleConfirmCancel">
            Cancelar
          </v-btn>
          <v-btn color="primary" elevated @click="handleConfirmOk">
            <v-icon left>mdi-check</v-icon>
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { OptionsQuestionItem, QuestionItem } from "~/domain/models/perspective/question/question";

export default Vue.extend({
  props: {
    questionsList: {
      type: Array as () => QuestionItem[],
      required: true,
    },
    optionsList: {
      type: Array as () => OptionsQuestionItem[],
      default: () => [],
    },
    projectId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // Armazena as respostas associadas ao ID da questão.
      // Para perguntas de texto, será uma string; para escolha múltipla, um número.
      answers: {} as Record<number, any>,
      // Controle da janela de confirmação
      confirmDialog: false,
    };
  },
  computed: {
    isFormValid(): boolean {
      return this.questionsList.every((question) => {
        const answer = this.answers[question.id];
        // Para perguntas de escolha múltipla (options_group !== null), verifica se o valor não é undefined ou null
        if (question.options_group !== null) {
          return answer !== undefined && answer !== null;
        } else {
          // Para perguntas de texto, verifica se há valor não vazio
          return typeof answer === "string" && answer.trim().length > 0;
        }
      });
    },
    answeredQuestions(): number {
      return this.questionsList.filter((question) => {
        const answer = this.answers[question.id];
        if (question.options_group !== null) {
          return answer !== undefined && answer !== null;
        } else {
          return typeof answer === "string" && answer.trim().length > 0;
        }
      }).length;
    },
    progressPercentage(): number {
      if (this.questionsList.length === 0) return 0;
      return (this.answeredQuestions / this.questionsList.length) * 100;
    }
  },
  methods: {
    getOptionsForQuestion(optionsGroup: number) {
      // Filtra as opções cujo options_group corresponde
      return this.optionsList.filter(option => option.options_group === optionsGroup);
    },
    openConfirmDialog() {
      this.confirmDialog = true;
    },
    handleConfirmOk() {
      // Fecha a janela de confirmação e submete as respostas
      this.confirmDialog = false;
      this.submit();
    },
    handleConfirmCancel() {
      // Fecha a janela de confirmação sem submeter
      this.confirmDialog = false;
    },
    submit() {
      const formattedAnswers = this.questionsList.map((question) => ({
        questionId: question.id,
        answer: this.answers[question.id],
        questionType: question.type, // assume que question.type é informado
      }));
      this.$emit("submit-answers", formattedAnswers, this.projectId);
      console.log("Respostas enviadas:", formattedAnswers);
    },
    clearAnswers() {
      // Reinicia o objeto answers
      this.answers = {} as Record<number, any>;
      console.log("Respostas limpas.");
    },
  },
});
</script>

<style scoped>
.form-answer-container {
  max-width: 800px;
  margin: 0 auto;
}

.empty-state-card {
  border-radius: 16px !important;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
}

.progress-card {
  border-radius: 12px !important;
  background: linear-gradient(145deg, #e3f2fd 0%, #bbdefb 100%);
}

.question-card {
  border-radius: 16px !important;
  transition: all 0.3s ease;
  border-left: 4px solid #1976d2;
}

.question-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
}

.question-header {
  background: linear-gradient(145deg, #f5f5f5 0%, #eeeeee 100%);
  border-radius: 12px 12px 0 0 !important;
  padding: 16px 20px;
}

.question-number {
  flex-shrink: 0;
}

.question-title {
  flex-grow: 1;
}

.options-container {
  padding: 8px 0;
}

.custom-radio-group {
  margin: 0;
}

.custom-radio {
  border-radius: 8px;
  padding: 8px 12px;
  margin: 4px 0;
  transition: all 0.2s ease;
}

.custom-radio:hover {
  background-color: rgba(25, 118, 210, 0.04);
}

.text-input-container {
  padding: 8px 0;
}

.custom-text-field {
  border-radius: 12px !important;
}

.actions-card {
  border-radius: 16px !important;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  border: 2px solid #e0e0e0;
}

.action-btn {
  border-radius: 24px !important;
  text-transform: none !important;
  font-weight: 600;
  padding: 0 24px;
  min-width: 160px;
}

.submit-btn {
  background: linear-gradient(145deg, #1976d2 0%, #1565c0 100%) !important;
}

.confirmation-dialog {
  border-radius: 20px !important;
  overflow: hidden;
}

.v-progress-linear {
  border-radius: 4px !important;
}

/* Melhorias nos radio buttons */
.v-radio ::v-deep .v-input--selection-controls__input {
  margin-right: 12px;
}

.v-radio ::v-deep .v-label {
  font-size: 16px;
  line-height: 1.4;
}

/* Efeitos de hover nos botões */
.v-btn:hover:not(.v-btn--disabled) {
  transform: translateY(-1px);
}

/* Animações */
.question-card {
  animation: slideInUp 0.3s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.v-dialog {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
