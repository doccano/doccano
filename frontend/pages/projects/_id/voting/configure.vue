<template>
  <v-container fluid>
    <!-- Database Error Alert - Always visible when database is down -->
    <v-alert
      v-if="!isDatabaseHealthy"
      ref="databaseAlert"
      type="error"
      prominent
      class="mb-4"
    >
      <v-row align="center">
        <v-col class="grow">
          <div class="title">De momento, a base de dados não se encontra disponível. Por favor, tente mais tarde.</div>
        </v-col>
        <v-col class="shrink">
          <v-icon size="48">mdi-database-alert</v-icon>
        </v-col>
      </v-row>
    </v-alert>

    <v-row>
      <v-col cols="12">
        <v-card>
                     <v-card-title>
             <v-btn
               icon
               class="mr-2"
               @click="$router.back()"
             >
               <v-icon>{{ mdiArrowLeft }}</v-icon>
             </v-btn>
             <h2>Configurar Votação</h2>
           </v-card-title>

                     <v-card-text>
             <v-form ref="form" v-model="valid" @submit.prevent>
               <v-row>
                 <!-- Voting Name -->
                 <v-col cols="12">
                   <v-text-field
                     v-model="configuration.name"
                     label="Nome da Votação"
                     placeholder="Insira um nome para esta sessão de votação"
                     outlined
                     :rules="[v => !!v || 'Campo obrigatório']"
                   >
                     <template #prepend>
                       <v-icon>{{ mdiVote }}</v-icon>
                     </template>
                   </v-text-field>
                 </v-col>

                 <!-- Description -->
                 <v-col cols="12">
                   <v-textarea
                     v-model="configuration.description"
                     label="Descrição da Votação"
                     placeholder="Descreva o propósito desta votação..."
                     outlined
                     rows="3"
                     :rules="[v => !!v || 'Campo obrigatório']"
                   >
                     <template #prepend>
                       <v-icon>{{ mdiText }}</v-icon>
                     </template>
                   </v-textarea>
                 </v-col>

                 <!-- Start Date -->
                 <v-col cols="12" md="6">
                   <v-menu
                     v-model="startDateMenu"
                     :close-on-content-click="false"
                     transition="scale-transition"
                     offset-y
                     min-width="auto"
                   >
                     <template #activator="{ on, attrs }">
                       <v-text-field
                         v-model="configuration.startDate"
                         label="Data de Início"
                         readonly
                         outlined
                         v-bind="attrs"
                         v-on="on"
                         :rules="[v => !!v || 'Campo obrigatório']"
                       >
                         <template #prepend>
                           <v-icon>{{ mdiCalendar }}</v-icon>
                         </template>
                       </v-text-field>
                     </template>
                     <v-date-picker
                       v-model="configuration.startDate"
                       @input="startDateMenu = false"
                     />
                   </v-menu>
                 </v-col>

                 <!-- End Date -->
                 <v-col cols="12" md="6">
                   <v-menu
                     v-model="endDateMenu"
                     :close-on-content-click="false"
                     transition="scale-transition"
                     offset-y
                     min-width="auto"
                   >
                     <template #activator="{ on, attrs }">
                       <v-text-field
                         v-model="configuration.endDate"
                         label="Data de Fim"
                         readonly
                         outlined
                         v-bind="attrs"
                         v-on="on"
                         :rules="[v => !!v || 'Campo obrigatório']"
                       >
                         <template #prepend>
                           <v-icon>{{ mdiCalendar }}</v-icon>
                         </template>
                       </v-text-field>
                     </template>
                     <v-date-picker
                       v-model="configuration.endDate"
                       @input="endDateMenu = false"
                     />
                   </v-menu>
                 </v-col>

                 <!-- Start Time -->
                 <v-col cols="12" md="6">
                   <v-menu
                     ref="startTimeMenu"
                     v-model="startTimeMenu"
                     :close-on-content-click="false"
                     :nudge-right="40"
                     :return-value.sync="configuration.startTime"
                     transition="scale-transition"
                     offset-y
                     max-width="290px"
                     min-width="290px"
                   >
                     <template #activator="{ on, attrs }">
                       <v-text-field
                         v-model="configuration.startTime"
                         label="Hora de Início"
                         readonly
                         outlined
                         v-bind="attrs"
                         v-on="on"
                         :rules="[v => !!v || 'Campo obrigatório']"
                       >
                         <template #prepend>
                           <v-icon>{{ mdiClock }}</v-icon>
                         </template>
                       </v-text-field>
                     </template>
                     <v-time-picker
                       v-if="startTimeMenu"
                       v-model="configuration.startTime"
                       full-width
                       @click:minute="$refs.startTimeMenu.save(configuration.startTime)"
                     />
                   </v-menu>
                 </v-col>

                 <!-- End Time -->
                 <v-col cols="12" md="6">
                   <v-menu
                     ref="endTimeMenu"
                     v-model="endTimeMenu"
                     :close-on-content-click="false"
                     :nudge-right="40"
                     :return-value.sync="configuration.endTime"
                     transition="scale-transition"
                     offset-y
                     max-width="290px"
                     min-width="290px"
                   >
                     <template #activator="{ on, attrs }">
                       <v-text-field
                         v-model="configuration.endTime"
                         label="Hora de Fim"
                         readonly
                         outlined
                         v-bind="attrs"
                         v-on="on"
                         :rules="[v => !!v || 'Campo obrigatório']"
                       >
                         <template #prepend>
                           <v-icon>{{ mdiClock }}</v-icon>
                         </template>
                       </v-text-field>
                     </template>
                     <v-time-picker
                       v-if="endTimeMenu"
                       v-model="configuration.endTime"
                       full-width
                       @click:minute="$refs.endTimeMenu.save(configuration.endTime)"
                     />
                   </v-menu>
                 </v-col>

                 <!-- Annotation Rules Section -->
                 <v-col cols="12" class="mt-6">
                   <v-divider class="mb-4" />
                   <h3 class="text-h6 mb-4">
                     <v-icon class="mr-2">{{ mdiFileDocumentEdit }}</v-icon>
                     Regras de Anotação
                   </h3>

                   <v-card outlined>
                     <v-card-text>
                       <div v-if="configuration.annotationRules.length === 0" class="text-center py-6">
                         <v-icon size="60" color="grey lighten-2">{{ mdiNoteText }}</v-icon>
                         <p class="text-body-2 grey--text mt-2">No annotation rules created yet.</p>
                         <p class="text-body-2 grey--text">Click the button below to add your first rule.</p>
                       </div>

                       <v-row v-for="(rule, index) in configuration.annotationRules" :key="index" class="mb-4">
                         <v-col cols="12">
                           <v-card 
                             outlined 
                             class="pa-4"
                             :class="rule.saved ? 'success lighten-5' : ''"
                           >
                             <!-- Saved Badge -->
                             <v-chip
                               v-if="rule.saved"
                               color="success"
                               small
                               class="mb-2"
                             >
                               <v-icon left small>{{ mdiCheck }}</v-icon>
                               Saved
                             </v-chip>
                             
                             <v-row>
                               <!-- Rule Name -->
                               <v-col cols="12" md="4">
                                 <v-text-field
                                   v-model="rule.name"
                                   label="Rule Name"
                                   placeholder="e.g., Entity Classification"
                                   outlined
                                   dense
                                   :disabled="rule.saved"
                                   :rules="[v => !!v || 'Required field']"
                                 >
                                   <template #prepend>
                                     <v-icon>{{ mdiTag }}</v-icon>
                                   </template>
                                 </v-text-field>
                               </v-col>

                               <!-- Rule Description -->
                               <v-col cols="12" md="7">
                                 <v-textarea
                                   v-model="rule.description"
                                   label="Rule Description"
                                   placeholder="Describe the annotation rule in detail..."
                                   outlined
                                   dense
                                   rows="3"
                                   :disabled="rule.saved"
                                   :rules="[v => !!v || 'Required field']"
                                 >
                                   <template #prepend>
                                     <v-icon>{{ mdiText }}</v-icon>
                                   </template>
                                 </v-textarea>
                               </v-col>

                               <!-- Action Buttons -->
                               <v-col cols="12" md="1" class="d-flex flex-column align-center">
                                 <!-- Edit Button (for saved rules) -->
                                 <v-btn
                                   v-if="rule.saved"
                                   icon
                                   color="primary"
                                   type="button"
                                   class="mb-1"
                                   @click="editRule(index)"
                                 >
                                   <v-icon>{{ mdiPencil }}</v-icon>
                                 </v-btn>
                                 
                                 <!-- Remove Button -->
                                 <v-btn
                                   icon
                                   color="red"
                                   type="button"
                                   :disabled="configuration.annotationRules.length <= 1 && !rule.saved"
                                   @click="removeRule(index)"
                                 >
                                   <v-icon>{{ mdiDelete }}</v-icon>
                                 </v-btn>
                               </v-col>
                             </v-row>
                           </v-card>
                         </v-col>
                       </v-row>

                       <!-- Save Rules Button -->
                       <div class="text-center mt-4" v-if="hasUnsavedRules">
                         <v-btn
                           color="success"
                           type="button"
                           @click="saveRules"
                           :disabled="!canSaveRules"
                         >
                           <v-icon left>{{ mdiContentSave }}</v-icon>
                           Save Rule
                         </v-btn>
                       </div>

                       <!-- Add Rule Button -->
                       <div class="text-center mt-4">
                         <v-btn
                           color="primary"
                           outlined
                           type="button"
                           @click="addRule"
                         >
                           <v-icon left>{{ mdiPlus }}</v-icon>
                           Add Annotation Rule
                         </v-btn>
                       </div>
                     </v-card-text>
                   </v-card>

                                      <v-alert
                     type="info"
                     text
                     :icon="false"
                     class="mt-4"
                   >
                     <strong>Note:</strong> These rules will be presented to annotators for voting. Be clear and specific about the annotation guidelines.
                   </v-alert>
                 </v-col>

                 <!-- How to Vote Section -->
                 <v-col cols="12" class="mt-8">
                   <v-divider class="mb-4" />
                   <h3 class="text-h6 mb-4">
                     <v-icon class="mr-2">{{ mdiVoteOutline }}</v-icon>
                     How to Vote
                   </h3>
                   
                   <v-card outlined>
                     <v-card-text>
                       <p class="text-body-2 grey--text mb-4">
                         Defina como os anotadores devem votar nas regras de anotação:
                       </p>
                       
                       <v-radio-group
                         v-model="configuration.votingMethod"
                         :rules="[v => !!v || 'Required field']"
                       >
                         <v-radio
                           value="approve_only"
                           color="success"
                         >
                           <template #label>
                             <div>
                               <strong>Aprovar apenas regras que concordam</strong>
                               <br>
                               <span class="text-body-2 grey--text">
                                 Anotadores só podem aprovar regras que apoiam. Regras não votadas permanecem neutras.
                               </span>
                             </div>
                           </template>
                         </v-radio>

                         <v-radio
                           value="disapprove_only"
                           color="error"
                           class="mt-4"
                         >
                           <template #label>
                             <div>
                               <strong>Reprovar apenas regras que discordam</strong>
                               <br>
                               <span class="text-body-2 grey--text">
                                 Anotadores só podem reprovar regras que se opõem. Regras não votadas permanecem neutras.
                               </span>
                             </div>
                           </template>
                         </v-radio>

                         <v-radio
                           value="approve_disapprove"
                           color="primary"
                           class="mt-4"
                         >
                           <template #label>
                             <div>
                               <strong>Aprovar ou reprovar todas as regras</strong>
                               <br>
                               <span class="text-body-2 grey--text">
                                 Anotadores devem votar em todas as regras - aprovar ou reprovar cada uma.
                               </span>
                             </div>
                           </template>
                         </v-radio>
                       </v-radio-group>
                     </v-card-text>
                   </v-card>

                   <v-alert
                     type="warning"
                     text
                     :icon="false"
                     class="mt-4"
                   >
                     <strong>Important:</strong> This voting method will determine how annotators interact with the rules during the voting session.
                   </v-alert>
                 </v-col>
               </v-row>
             </v-form>
           </v-card-text>

           <!-- Action Buttons at the bottom -->
           <v-card-actions class="px-6 pb-6">
             <v-spacer />
             
             <!-- Cancel Button -->
             <v-btn
               color="error"
               class="mr-3"
               @click="cancelConfiguration"
             >
               <v-icon left>{{ mdiClose }}</v-icon>
               Cancel
             </v-btn>
             
             <!-- Save Configuration Button -->
             <v-btn
               color="success"
               :loading="saving"
               @click="saveConfiguration"
             >
               <v-icon left>{{ mdiCheck }}</v-icon>
               Save Configuration
             </v-btn>
           </v-card-actions>
         </v-card>
       </v-col>
     </v-row>

     <!-- Delete Confirmation Dialog -->
     <v-dialog v-model="showDeleteDialog" max-width="400px" persistent>
       <v-card>
         <v-card-title class="headline error--text">
           <v-icon class="mr-2" color="error">{{ mdiDelete }}</v-icon>
           Delete Rule?
         </v-card-title>
         
         <v-card-text class="pt-4">
           <p class="text-body-1">
             Are you sure you want to delete the rule:
           </p>
           <p class="font-weight-bold text-h6 primary--text">
             "{{ ruleToDelete?.name }}"
           </p>
           <p class="text-body-2 grey--text">
             This action cannot be undone.
           </p>
         </v-card-text>
         
         <v-card-actions>
           <v-spacer />
           <v-btn
             text
             @click="cancelDelete"
           >
             Cancel
           </v-btn>
           <v-btn
             color="error"
             @click="confirmDelete"
           >
             <v-icon left>{{ mdiDelete }}</v-icon>
             Delete
           </v-btn>
         </v-card-actions>
       </v-card>
     </v-dialog>
   </v-container>
 </template>

<script>
import {
  mdiArrowLeft,
  mdiCheck,
  mdiClose,
  mdiVote,
  mdiClock,
  mdiText,
  mdiCalendar,
  mdiFileDocumentEdit,
  mdiNoteText,
  mdiTag,
  mdiDelete,
  mdiPlus,
  mdiContentSave,
  mdiPencil,
  mdiVoteOutline
} from '@mdi/js'
import { databaseHealthMixin } from '@/mixins/databaseHealthMixin'

export default {
  mixins: [databaseHealthMixin],
  layout: 'project',

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      mdiArrowLeft,
      mdiCheck,
      mdiClose,
      mdiVote,
      mdiClock,
      mdiText,
      mdiCalendar,
      mdiFileDocumentEdit,
      mdiNoteText,
      mdiTag,
      mdiDelete,
      mdiPlus,
      mdiContentSave,
      mdiPencil,
      mdiVoteOutline,
      valid: false,
      saving: false,
      startDateMenu: false,
      endDateMenu: false,
      startTimeMenu: false,
      endTimeMenu: false,
      showDeleteDialog: false,
      ruleToDelete: null,
      ruleIndexToDelete: null,
      editingConfigId: null,
      configuration: {
        name: '',
        description: '',
        startDate: '',
        endDate: '',
        startTime: '',
        endTime: '',
        annotationRules: [],
        votingMethod: ''
      }
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      await this.$services.project.findById(this.$route.params.id)
      
      // Check if we're editing an existing configuration
      const editingConfigId = sessionStorage.getItem('editingConfigId')
      if (editingConfigId) {
        this.loadExistingConfiguration(editingConfigId)
        sessionStorage.removeItem('editingConfigId')
      }
    } catch(e) {
      throw new Error(e.response.data.detail)
    } finally {
      this.isLoading = false
    }
  },

  mounted() {
    // Set default dates and times only if not editing
    if (!this.editingConfigId) {
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)

      this.configuration.startDate = today.toISOString().substr(0, 10)
      this.configuration.endDate = tomorrow.toISOString().substr(0, 10)
      this.configuration.startTime = '09:00'
      this.configuration.endTime = '17:00'

      // Add a default annotation rule
      this.configuration.annotationRules.push({
        name: '',
        description: '',
        saved: false
      })
    }
  },

  head() {
    return {
      title: 'Configure Voting'
    }
  },

  watch: {
    isDatabaseHealthy(newValue, oldValue) {
      // Se a base de dados ficou indisponível (mudou de true para false)
      if (oldValue === true && newValue === false) {
        // Aguarda o próximo tick para garantir que o alerta foi renderizado
        this.$nextTick(() => {
          // Faz scroll para o topo da página para mostrar o alerta
          window.scrollTo({
            top: 0,
            behavior: 'smooth'
          })
        })
      }
    }
  },

  computed: {
    project() {
      return this.$store.getters['projects/project']
    },
    
    isProjectAdmin() {
      return this.$store.getters['projects/isProjectAdmin']
    },

    hasUnsavedRules() {
      return this.configuration.annotationRules.some(rule => !rule.saved)
    },

    canSaveRules() {
      return this.configuration.annotationRules.some(rule => 
        !rule.saved && rule.name.trim() && rule.description.trim()
      )
    }
  },

  methods: {
    addRule() {
      this.configuration.annotationRules.push({
        name: '',
        description: '',
        saved: false
      })
    },

    removeRule(index) {
      console.log('removeRule called with index:', index)
      console.log('Current rules length:', this.configuration.annotationRules.length)
      
      const rule = this.configuration.annotationRules[index]
      console.log('Rule to remove:', rule)
      
      // Can remove if:
      // 1. There are more than 1 rules, OR
      // 2. There's only 1 rule but it's saved (can delete saved rules)
      const canRemove = this.configuration.annotationRules.length > 1 || rule.saved
      
      if (canRemove) {
        // If rule is saved, show confirmation dialog
        if (rule.saved) {
          this.ruleToDelete = rule
          this.ruleIndexToDelete = index
          this.showDeleteDialog = true
        } else {
          // If not saved, remove directly
          this.configuration.annotationRules.splice(index, 1)
          console.log('Unsaved rule removed! New length:', this.configuration.annotationRules.length)
        }
      } else {
        console.log('Cannot remove: only one unsaved rule remaining')
      }
    },

    editRule(index) {
      // Set the rule back to unsaved state to allow editing
      this.configuration.annotationRules[index].saved = false
    },

    confirmDelete() {
      console.log('Confirming delete for rule:', this.ruleToDelete)
      
      if (this.ruleIndexToDelete !== null) {
        this.configuration.annotationRules.splice(this.ruleIndexToDelete, 1)
        console.log('Rule removed! New length:', this.configuration.annotationRules.length)
        
        // If no rules left, add a new empty one
        if (this.configuration.annotationRules.length === 0) {
          this.addRule()
          console.log('Added new empty rule after deleting all')
        }
      }
      
      this.cancelDelete()
    },

    cancelDelete() {
      this.showDeleteDialog = false
      this.ruleToDelete = null
      this.ruleIndexToDelete = null
    },

    saveRules() {
      this.configuration.annotationRules.forEach(rule => {
        if (!rule.saved && rule.name.trim() && rule.description.trim()) {
          rule.saved = true
        }
      })
    },

    cancelConfiguration() {
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting`))
    },

    loadExistingConfiguration(configId) {
      const savedConfigs = localStorage.getItem(`voting_configs_${this.$route.params.id}`)
      if (savedConfigs) {
        const configs = JSON.parse(savedConfigs)
        const config = configs.find(c => c.id.toString() === configId)
        if (config) {
          this.configuration = { ...config }
          this.editingConfigId = configId
        }
      }
    },

    async saveConfiguration() {
      if (!this.$refs.form.validate()) {
        return
      }

      this.saving = true
      try {
        // Get existing configurations array
        const existingConfigs = JSON.parse(localStorage.getItem(`voting_configs_${this.$route.params.id}`) || '[]')
        
        if (this.editingConfigId) {
          // Update existing configuration
          const configIndex = existingConfigs.findIndex(c => c.id.toString() === this.editingConfigId)
          if (configIndex !== -1) {
            const configToSave = {
              ...this.configuration,
              id: parseInt(this.editingConfigId),
              projectId: this.$route.params.id,
              updatedAt: new Date().toISOString(),
              status: 'configured'
            }
            existingConfigs[configIndex] = configToSave
            console.log('Configuration updated:', configToSave)
          }
        } else {
          // Create new configuration
          const configToSave = {
            ...this.configuration,
            id: Date.now(), // Simple ID generation
            projectId: this.$route.params.id,
            createdAt: new Date().toISOString(),
            status: 'configured'
          }
          existingConfigs.push(configToSave)
          console.log('Configuration created:', configToSave)
        }
        
        localStorage.setItem(`voting_configs_${this.$route.params.id}`, JSON.stringify(existingConfigs))
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting`))
      } catch (error) {
        console.error('Error saving configuration:', error)
      } finally {
        this.saving = false
      }
    }
  }
}
</script> 