<template>
  <v-dialog
    :value="value"
    max-width="800px"
    persistent
    @input="$emit('input', $event)"
  >
    <v-card>
      <v-card-title class="headline">
        Configurar Nova Votação
      </v-card-title>

      <v-card-text>
        <v-form ref="form" class="mt-4">
          <!-- Datas de início e fim -->
          <v-row>
            <v-col cols="12" sm="6">
              <v-menu
                v-model="startDateMenu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template #activator="{ on, attrs }">
                  <v-text-field
                    v-model="startDate"
                    label="Data de Início"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    :rules="startDateRules"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="startDate"
                  :max="endDate"
                  @input="startDateMenu = false"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12" sm="6">
              <v-menu
                v-model="endDateMenu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template #activator="{ on, attrs }">
                  <v-text-field
                    v-model="endDate"
                    label="Data de Fim"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    :rules="endDateRules"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="endDate"
                  :min="startDate"
                  @input="endDateMenu = false"
                ></v-date-picker>
              </v-menu>
            </v-col>
          </v-row>

          <!-- Descrição da votação -->
          <v-textarea
            v-model="description"
            label="Descrição da Votação"
            rows="4"
            placeholder="Digite a descrição da votação..."
            required
            :rules="descriptionRules"
            class="mt-4"
          />

          <!-- Seleção de regras de anotação -->
          <v-card outlined class="mt-4">
            <v-card-title class="subtitle-1">
              Regras de Anotação
            </v-card-title>
            <v-card-text>
              <v-alert
                v-if="availableRules.length === 0"
                type="info"
                outlined
                class="mb-4"
              >
                Você precisa criar regras de anotação para configurar a votação. Use o botão abaixo para criar novas regras.
              </v-alert>
              
              <v-list v-else>
                <v-list-item
                  v-for="rule in availableRules"
                  :key="rule.id"
                >
                  <v-checkbox
                    v-model="selectedRules"
                    :value="rule.id"
                    hide-details
                    class="mr-2"
                  ></v-checkbox>
                  <div>
                    <div class="font-weight-medium">{{ rule.name }}</div>
                    <div class="text-caption">{{ rule.description }}</div>
                  </div>
                </v-list-item>
              </v-list>
              
              <v-btn
                :color="availableRules.length === 0 ? 'primary' : 'secondary'"
                :outlined="availableRules.length === 0"
                class="mt-4"
                @click="showNewRuleForm = true"
              >
                <v-icon left>mdi-plus</v-icon>
                Criar Nova Regra
              </v-btn>
            </v-card-text>
          </v-card>

          <!-- Formulário para criar nova regra -->
          <NewRuleForm 
            v-if="showNewRuleForm"
            @cancel="showNewRuleForm = false"
            @save="handleNewRule"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="secondary"
          text
          @click="$emit('input', false)"
        >
          Cancelar
        </v-btn>
        <v-btn
          :loading="saving"
          color="primary"
          :disabled="!isFormValid"
          @click="saveConfig"
        >
          Salvar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import NewRuleForm from './NewRuleForm.vue'

interface AnnotationRule {
  id: number;
  name: string;
  description: string;
}

interface NewRule {
  name: string;
  description: string;
}

export default defineComponent({
  name: 'VotingConfigModal',
  
  components: {
    NewRuleForm
  },
  
  props: {
    value: {
      type: Boolean,
      required: true
    },
    projectId: {
      type: [String, Number],
      default: null
    }
  },
  
  data() {
    return {
      form: null,
      startDate: '',
      endDate: '',
      startDateMenu: false,
      endDateMenu: false,
      description: '',
      selectedRules: [] as number[],
      showNewRuleForm: false,
      saving: false,
      
      // Regras de validação
      startDateRules: [
        (v: any) => !!v || 'Data de início é obrigatória'
      ],
      
      endDateRules: [
        (v: any) => !!v || 'Data de fim é obrigatória'
      ],
      
      descriptionRules: [
        (v: any) => !!v || 'Descrição é obrigatória'
      ]
    }
  },
  
  computed: {
    ...mapGetters({
      annotationRules: 'voting/annotationRules'
    }),
    
    availableRules(): AnnotationRule[] {
      return this.annotationRules || []
    },
    
    isFormValid(): boolean {
      return Boolean(
        this.startDate && 
        this.endDate && 
        this.description && 
        this.selectedRules.length > 0
      )
    }
  },
  
  mounted() {
    if (this.projectId) {
      this.$store.dispatch('voting/initVotingState', this.projectId)
    }
  },
  
  methods: {
    async handleNewRule(newRule: NewRule) {
      // Salvar a regra na store
      const result = await this.$store.dispatch('voting/createAnnotationRule', {
        projectId: this.projectId,
        rule: newRule
      })
      
      if (result.success) {
        // Selecionar automaticamente a nova regra
        this.selectedRules.push(result.data.id)
        this.showNewRuleForm = false
      }
    },
    
    async saveConfig() {
      // Verificar se o formulário é válido
      if (this.$refs.form && this.isFormValid) {
        this.saving = true
        try {
          // Criar objeto de configuração de votação
          const votingData = {
            startDate: this.startDate,
            endDate: this.endDate,
            description: this.description,
            rules: this.selectedRules
          }
          
          // Salvar na store
          const result = await this.$store.dispatch('voting/createVoting', {
            projectId: this.projectId,
            votingData
          })
          
          if (result.success) {
            // Limpar formulário
            this.startDate = ''
            this.endDate = ''
            this.description = ''
            this.selectedRules = []
            
            // Notificar componente pai do sucesso
            this.$emit('saved', result.data)
            
            // Fechar modal
            this.$emit('input', false)
          }
        } catch (error) {
          console.error('Erro ao salvar configuração de votação:', error)
        } finally {
          this.saving = false
        }
      }
    }
  }
})
</script>

<style scoped>
/* Sem necessidade da classe v-datetime-picker */
</style> 