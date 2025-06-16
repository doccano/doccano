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
            <h2>Votação</h2>
          </v-card-title>

          <v-card-text>
            <!-- Interface para Administradores -->
            <div v-if="isProjectAdmin">
              <!-- Header with Create Button -->
              <div class="d-flex justify-space-between align-center mb-6">
                <div>
                  <p class="text-body-2 grey--text mb-0">
                    Gerenciar configurações de votação
                  </p>
                </div>
                <v-btn
                  :color="canConfigureVoting ? 'primary' : 'grey'"
                  :disabled="!canConfigureVoting"
                  @click="goToConfiguration"
                >
                  <v-icon left>{{ mdiPlus }}</v-icon>
                  Criar Nova Votação
                </v-btn>
              </div>

              <!-- Configurations List -->
              <div v-if="votingConfigurations.length > 0">
                <v-expansion-panels multiple>
                  <v-expansion-panel
                    v-for="(config, index) in votingConfigurations"
                    :key="config.id"
                  >
                    <v-expansion-panel-header>
                      <div class="d-flex align-center">
                        <v-icon class="mr-3" color="primary">{{ mdiVote }}</v-icon>
                        <div>
                          <div class="font-weight-bold">{{ config.name }}</div>
                          <div class="text-body-2 grey--text">
                            {{ formatDate(config.startDate) }} - {{ formatDate(config.endDate) }} | 
                            {{ config.annotationRules.length }} regras
                          </div>
                        </div>
                        <v-spacer />
                        <v-chip
                          :color="getVotingStatusColor(config)"
                          dark
                          small
                          class="mr-2"
                        >
                          {{ getVotingStatusText(config) }}
                        </v-chip>
                        <v-chip
                          :color="getVotingMethodColor(config.votingMethod)"
                          dark
                          small
                          class="mr-2"
                        >
                          {{ getVotingMethodText(config.votingMethod) }}
                        </v-chip>
                      </div>
                    </v-expansion-panel-header>

                    <v-expansion-panel-content>
                      <v-card flat>
                        <v-card-text class="pa-0 pt-4">
                          <v-row>
                            <!-- Basic Information -->
                            <v-col cols="12" md="6">
                              <h4 class="text-h6 mb-3">Informações Básicas</h4>
                              <div class="mb-2">
                                <strong>Descrição:</strong> {{ config.description }}
                              </div>
                              <div class="mb-2">
                                <strong>Período:</strong> {{ formatDate(config.startDate) }} - {{ formatDate(config.endDate) }}
                              </div>
                              <div class="mb-2">
                                <strong>Horário:</strong> {{ config.startTime }} - {{ config.endTime }}
                              </div>
                              <div class="mb-2">
                                <strong>Criado em:</strong> {{ formatDateTime(config.createdAt) }}
                              </div>
                            </v-col>

                            <!-- Voting Method -->
                            <v-col cols="12" md="6">
                              <h4 class="text-h6 mb-3">Método de Votação</h4>
                              <v-chip
                                :color="getVotingMethodColor(config.votingMethod)"
                                dark
                                class="mb-2"
                              >
                                {{ getVotingMethodText(config.votingMethod) }}
                              </v-chip>
                              <p class="text-body-2 grey--text mt-2">
                                {{ getVotingMethodDescription(config.votingMethod) }}
                              </p>
                            </v-col>

                            <!-- Annotation Rules -->
                            <v-col cols="12">
                              <h4 class="text-h6 mb-3">Regras de Anotação ({{ config.annotationRules.length }})</h4>
                              <v-row>
                                <v-col
                                  v-for="(rule, ruleIndex) in config.annotationRules"
                                  :key="ruleIndex"
                                  cols="12"
                                  md="6"
                                >
                                  <v-card outlined class="mb-2">
                                    <v-card-text class="py-3">
                                      <div class="font-weight-bold text-subtitle-2 mb-1">
                                        {{ rule.name }}
                                      </div>
                                      <div class="text-body-2 grey--text">
                                        {{ rule.description }}
                                      </div>
                                    </v-card-text>
                                  </v-card>
                                </v-col>
                              </v-row>
                            </v-col>

                            <!-- Voting Results (for admins) -->
                            <v-col v-if="getVotingResults(config.id)" cols="12">
                              <v-divider class="my-4" />
                              <h4 class="text-h6 mb-3">Resultados da Votação</h4>
                              <v-card outlined>
                                <v-card-text>
                                  <div v-for="(rule, ruleIndex) in config.annotationRules" :key="ruleIndex" class="mb-4">
                                    <div class="font-weight-bold mb-2">{{ rule.name }}</div>
                                    <div class="mb-2">
                                      <v-chip 
                                        color="success" 
                                        small 
                                        class="mr-2"
                                      >
                                        <v-icon left small>mdi-thumb-up</v-icon>
                                        Aprovações: {{ getRuleVotes(config.id, ruleIndex, 'approve') }}
                                      </v-chip>
                                      <v-chip 
                                        color="error" 
                                        small 
                                        class="mr-2"
                                      >
                                        <v-icon left small>mdi-thumb-down</v-icon>
                                        Reprovações: {{ getRuleVotes(config.id, ruleIndex, 'disapprove') }}
                                      </v-chip>
                                      <v-chip 
                                        color="grey" 
                                        small
                                      >
                                        <v-icon left small>mdi-minus</v-icon>
                                        Neutros: {{ getRuleVotes(config.id, ruleIndex, 'neutral') }}
                                      </v-chip>
                                    </div>
                                    <v-progress-linear
                                      :value="getRuleApprovalPercentage(config.id, ruleIndex)"
                                      height="8"
                                      color="success"
                                      background-color="error"
                                      class="mb-1"
                                    />
                                    <div class="text-caption grey--text">
                                      {{ getRuleApprovalPercentage(config.id, ruleIndex).toFixed(1) }}% de aprovação
                                    </div>
                                  </div>
                                  
                                  <v-divider class="my-3" />
                                  <div class="text-center">
                                    <strong>Total de Participantes: {{ getTotalParticipants(config.id) }}</strong>
                                  </div>
                                </v-card-text>
                              </v-card>
                            </v-col>
                          </v-row>

                          <!-- Actions -->
                          <v-divider class="my-4" />
                          <div class="d-flex justify-space-between">
                            <div>
                              <v-btn
                                color="primary"
                                outlined
                                class="mr-2"
                                @click="editConfiguration(config)"
                              >
                                <v-icon left>{{ mdiPencil }}</v-icon>
                                Editar Configuração
                              </v-btn>
                              
                              <v-btn
                                v-if="getVotingResults(config.id)"
                                color="info"
                                outlined
                                @click="viewDetailedResults(config)"
                              >
                                <v-icon left>mdi-chart-bar</v-icon>
                                Ver Resultados Detalhados
                              </v-btn>
                            </div>
                            
                            <v-btn
                              color="error"
                              outlined
                              @click="deleteConfiguration(config, index)"
                            >
                              <v-icon left>{{ mdiDelete }}</v-icon>
                              Excluir
                            </v-btn>
                          </div>
                        </v-card-text>
                      </v-card>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>

              <!-- Empty State for Admins -->
              <div v-else class="text-center pa-12">
                <v-icon size="120" color="grey lighten-1">
                  {{ mdiVote }}
                </v-icon>
                <h3 class="text-h5 grey--text text--darken-1 mt-4">
                  Nenhuma Configuração de Votação
                </h3>
                <p class="text-body-1 grey--text mt-2">
                  Crie sua primeira configuração de votação para começar.
                </p>
              </div>

              <!-- Status message for admins -->
              <div class="mt-6 text-center">
                <v-alert
                  v-if="!hasDiscussions"
                  type="info"
                  text
                  class="mb-0"
                  :icon="false"
                >
                  <strong>Ainda não há discussões criadas.</strong><br>
                  Crie uma discussão primeiro para habilitar a configuração de votação.
                  <br><br>
                  <v-btn
                    color="primary"
                    small
                    outlined
                    @click="goToDiscussions"
                  >
                    Ir para Discussões
                  </v-btn>
                </v-alert>
                
                <v-alert
                  v-else-if="openDiscussions.length > 0"
                  type="warning"
                  text
                  class="mb-0"
                  :icon="false"
                >
                  <strong>{{ openDiscussions.length }} discussão(ões) atualmente abertas.</strong><br>
                  Feche todas as discussões para habilitar a configuração de votação.
                  <br><br>
                  <v-btn
                    color="orange"
                    small
                    outlined
                    @click="goToDiscussions"
                  >
                    Gerenciar Discussões
                  </v-btn>
                </v-alert>
                
                <v-alert
                  v-else-if="votingConfigurations.length === 0"
                  type="success"
                  text
                  class="mb-0"
                  :icon="false"
                >
                  <strong>Pronto para criar votações!</strong><br>
                  Todas as discussões estão fechadas. Você pode criar uma nova configuração de votação.
                </v-alert>
              </div>
            </div>

            <!-- Interface para Usuários -->
            <div v-else>
              <div class="mb-6">
                <h3 class="text-h5 mb-2">Votações Disponíveis</h3>
                <p class="text-body-2 grey--text">
                  Vote nas regras de anotação para contribuir com o projeto.
                </p>
              </div>

              <!-- Active Voting for Users -->
              <div v-if="activeVotingForUsers.length > 0">
                <v-card
                  v-for="config in activeVotingForUsers"
                  :key="config.id"
                  class="mb-4"
                  outlined
                >
                  <v-card-title>
                    <v-icon class="mr-3" color="primary">{{ mdiVote }}</v-icon>
                    {{ config.name }}
                    <v-spacer />
                    <v-chip color="success" dark small>
                      <v-icon left small>mdi-clock</v-icon>
                      Ativa
                    </v-chip>
                  </v-card-title>
                  
                  <v-card-subtitle>
                    {{ config.description }}
                  </v-card-subtitle>

                  <v-card-text>
                    <div class="mb-4">
                      <v-chip
                        :color="getVotingMethodColor(config.votingMethod)"
                        dark
                        small
                        class="mb-2"
                      >
                        {{ getVotingMethodText(config.votingMethod) }}
                      </v-chip>
                      <p class="text-body-2 grey--text mt-2">
                        {{ getVotingMethodDescription(config.votingMethod) }}
                      </p>
                    </div>

                    <div class="mb-4">
                      <strong>Período:</strong> {{ formatDate(config.startDate) }} - {{ formatDate(config.endDate) }}<br>
                      <strong>Horário:</strong> {{ config.startTime }} - {{ config.endTime }}
                    </div>

                    <v-divider class="my-4" />

                    <h4 class="text-h6 mb-4">Regras de Anotação</h4>
                    
                    <div v-for="(rule, ruleIndex) in config.annotationRules" :key="ruleIndex" class="mb-6">
                      <v-card outlined class="mb-3">
                        <v-card-text>
                          <h5 class="text-subtitle-1 font-weight-bold mb-2">
                            {{ rule.name }}
                          </h5>
                          <p class="text-body-2 mb-3">
                            {{ rule.description }}
                          </p>
                          
                          <!-- Voting Controls -->
                          <div class="d-flex align-center">
                            <span class="text-body-2 mr-4 font-weight-medium">Seu voto:</span>
                            
                            <!-- Current status indicator -->
                            <v-chip
                              v-if="!reactiveUserVotes[`${config.id}_${ruleIndex}`]"
                              color="grey lighten-1"
                              small
                              outlined
                              class="mr-3"
                            >
                              <v-icon left small>mdi-help-circle-outline</v-icon>
                              Não votado
                            </v-chip>
                            
                            <!-- Vote status chip when voted -->
                            <v-chip
                              v-else
                              :key="`status-${config.id}-${ruleIndex}-${reactiveUserVotes[`${config.id}_${ruleIndex}`]}`"
                              :color="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'success' : 'error'"
                              small
                              dark
                              class="mr-3"
                            >
                              <v-icon left small>
                                {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'mdi-check-circle' : 'mdi-close-circle' }}
                              </v-icon>
                              {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'Aprovado' : 'Reprovado' }}
                            </v-chip>
                            
                            <!-- Approve/Disapprove Toggle -->
                            <div v-if="config.votingMethod === 'approve_disapprove'" class="d-flex">
                              <v-btn
                                :key="`approve-${config.id}-${ruleIndex}-${reactiveUserVotes[`${config.id}_${ruleIndex}`] || 'none'}`"
                                :color="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'success' : 'grey lighten-1'"
                                :dark="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve'"
                                :outlined="reactiveUserVotes[`${config.id}_${ruleIndex}`] !== 'approve'"
                                small
                                class="mr-2 vote-button"
                                :class="{
                                  'vote-selected': reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve',
                                  'vote-approve': reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve'
                                }"
                                @click="vote(config.id, ruleIndex, reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? null : 'approve')"
                              >
                                <v-icon small class="mr-1">
                                  {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'mdi-check-circle' : 'mdi-thumb-up' }}
                                </v-icon>
                                {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'APROVADO ✓' : 'APROVAR' }}
                              </v-btn>
                              
                              <v-btn
                                :key="`disapprove-${config.id}-${ruleIndex}-${reactiveUserVotes[`${config.id}_${ruleIndex}`] || 'none'}`"
                                :color="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove' ? 'error' : 'grey lighten-1'"
                                :dark="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove'"
                                :outlined="reactiveUserVotes[`${config.id}_${ruleIndex}`] !== 'disapprove'"
                                small
                                class="vote-button"
                                :class="{
                                  'vote-selected': reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove',
                                  'vote-disapprove': reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove'
                                }"
                                @click="vote(config.id, ruleIndex, reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove' ? null : 'disapprove')"
                              >
                                <v-icon small class="mr-1">
                                  {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove' ? 'mdi-close-circle' : 'mdi-thumb-down' }}
                                </v-icon>
                                {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove' ? 'REPROVADO ✗' : 'REPROVAR' }}
                              </v-btn>
                            </div>

                            <!-- Approve Only -->
                            <div v-else-if="config.votingMethod === 'approve_only'">
                              <v-btn
                                :key="`approve-only-${config.id}-${ruleIndex}-${reactiveUserVotes[`${config.id}_${ruleIndex}`] || 'none'}`"
                                :color="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'success' : 'grey lighten-1'"
                                :dark="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve'"
                                :outlined="reactiveUserVotes[`${config.id}_${ruleIndex}`] !== 'approve'"
                                small
                                class="vote-button"
                                :class="{
                                  'vote-selected': reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve',
                                  'vote-approve': reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve'
                                }"
                                @click="vote(config.id, ruleIndex, reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? null : 'approve')"
                              >
                                <v-icon small class="mr-1">
                                  {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'mdi-check-circle' : 'mdi-thumb-up' }}
                                </v-icon>
                                {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'APROVADO ✓' : 'APROVAR' }}
                              </v-btn>
                            </div>

                            <!-- Disapprove Only -->
                            <div v-else-if="config.votingMethod === 'disapprove_only'">
                              <v-btn
                                :key="`disapprove-only-${config.id}-${ruleIndex}-${reactiveUserVotes[`${config.id}_${ruleIndex}`] || 'none'}`"
                                :color="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove' ? 'error' : 'grey lighten-1'"
                                :dark="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove'"
                                :outlined="reactiveUserVotes[`${config.id}_${ruleIndex}`] !== 'disapprove'"
                                small
                                class="vote-button"
                                :class="{
                                  'vote-selected': reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove',
                                  'vote-disapprove': reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove'
                                }"
                                @click="vote(config.id, ruleIndex, reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove' ? null : 'disapprove')"
                              >
                                <v-icon small class="mr-1">
                                  {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove' ? 'mdi-close-circle' : 'mdi-thumb-down' }}
                                </v-icon>
                                {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'disapprove' ? 'REPROVADO ✗' : 'REPROVAR' }}
                              </v-btn>
                            </div>
                          </div>
                          
                          <!-- Vote status indicator -->
                          <div class="mt-3">
                            <!-- When user has voted -->
                            <v-alert
                              v-if="reactiveUserVotes[`${config.id}_${ruleIndex}`]"
                              :type="reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'success' : 'error'"
                              dense
                              text
                              class="mb-0"
                            >
                              <div class="d-flex align-center">
                                <v-icon small class="mr-2">
                                  {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'mdi-check-circle' : 'mdi-close-circle' }}
                                </v-icon>
                                <span class="text-body-2">
                                  <strong>Voto registrado:</strong> Você {{ reactiveUserVotes[`${config.id}_${ruleIndex}`] === 'approve' ? 'aprovou' : 'reprovou' }} esta regra.
                                  <span class="font-weight-medium">
                                    Clique novamente para alterar.
                                  </span>
                                </span>
                              </div>
                            </v-alert>
                            
                            <!-- When user hasn't voted yet -->
                            <v-alert
                              v-else
                              type="info"
                              dense
                              outlined
                              class="mb-0"
                            >
                              <div class="d-flex align-center">
                                <v-icon small class="mr-2">mdi-information-outline</v-icon>
                                <span class="text-body-2">
                                  <span v-if="config.votingMethod === 'approve_disapprove'">
                                    <strong>Clique em "APROVAR" ou "REPROVAR"</strong> para registrar seu voto nesta regra.
                                  </span>
                                  <span v-else-if="config.votingMethod === 'approve_only'">
                                    <strong>Clique em "APROVAR"</strong> se concordar com esta regra. Caso contrário, deixe sem voto.
                                  </span>
                                  <span v-else-if="config.votingMethod === 'disapprove_only'">
                                    <strong>Clique em "REPROVAR"</strong> se discordar desta regra. Caso contrário, deixe sem voto.
                                  </span>
                                </span>
                              </div>
                            </v-alert>
                          </div>
                        </v-card-text>
                      </v-card>
                    </div>

                    <v-alert
                      type="info"
                      text
                      class="mt-4"
                    >
                      <v-icon slot="prepend">mdi-information</v-icon>
                      Seus votos são salvos automaticamente. Você pode alterá-los a qualquer momento durante o período de votação.
                    </v-alert>
                  </v-card-text>
                </v-card>
              </div>

              <!-- No Active Voting for Users -->
              <div v-else class="text-center pa-12">
                <v-icon size="120" color="grey lighten-1">
                  {{ mdiVote }}
                </v-icon>
                <h3 class="text-h5 grey--text text--darken-1 mt-4">
                  Nenhuma Votação Ativa
                </h3>
                <p class="text-body-1 grey--text mt-2">
                  Não há votações disponíveis no momento. Aguarde o administrador criar uma nova votação.
                </p>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Detailed Results Dialog -->
    <v-dialog v-model="showResultsDialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Resultados Detalhados - {{ selectedConfig?.name }}</span>
          <v-spacer />
          <v-btn icon @click="showResultsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text>
          <div v-if="selectedConfig">
            <div v-for="(rule, ruleIndex) in selectedConfig.annotationRules" :key="ruleIndex" class="mb-6">
              <h4 class="text-h6 mb-3">{{ rule.name }}</h4>
              <p class="text-body-2 grey--text mb-3">{{ rule.description }}</p>
              
              <v-row>
                <v-col cols="12" md="6">
                  <v-card outlined>
                    <v-card-text>
                      <div class="text-center">
                        <div class="text-h4 success--text">
                          {{ getRuleVotes(selectedConfig.id, ruleIndex, 'approve') }}
                        </div>
                        <div class="text-body-2">Aprovações</div>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="12" md="6">
                  <v-card outlined>
                    <v-card-text>
                      <div class="text-center">
                        <div class="text-h4 error--text">
                          {{ getRuleVotes(selectedConfig.id, ruleIndex, 'disapprove') }}
                        </div>
                        <div class="text-body-2">Reprovações</div>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
              
              <v-progress-linear
                :value="getRuleApprovalPercentage(selectedConfig.id, ruleIndex)"
                height="20"
                color="success"
                background-color="error"
                class="mt-3"
              >
                <template #default="{ value }">
                  <strong class="white--text">{{ Math.ceil(value) }}% aprovação</strong>
                </template>
              </v-progress-linear>
              
              <v-divider v-if="ruleIndex < selectedConfig.annotationRules.length - 1" class="my-4" />
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Confirmation Dialog for Active Voting -->
    <v-dialog v-model="showActiveVotingDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title class="text-h5">
          <v-icon left color="warning">{{ mdiAlert }}</v-icon>
          Votação Ativa Encontrada
        </v-card-title>
        
        <v-card-text>
          <p class="mb-3">
            <strong>Há uma votação ativa no momento:</strong>
          </p>
          <v-card outlined class="mb-3">
            <v-card-text class="py-2">
              <div class="font-weight-bold">{{ activeVotingConfig?.name }}</div>
              <div class="text-body-2 grey--text">
                {{ formatDate(activeVotingConfig?.startDate) }} - {{ formatDate(activeVotingConfig?.endDate) }}
              </div>
            </v-card-text>
          </v-card>
          <p class="mb-0">
            Apenas uma votação pode estar ativa por vez. Deseja encerrar a votação anterior antecipadamente e configurar uma nova?
          </p>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn
            text
            @click="cancelNewVoting"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="warning"
            @click="terminateAndCreateNew"
          >
            Encerrar e Criar Nova
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import {
  mdiVote,
  mdiCog,
  mdiCheckCircle,
  mdiPencil,
  mdiPlus,
  mdiDelete,
  mdiAlert
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
      mdiVote,
      mdiCog,
      mdiCheckCircle,
      mdiPencil,
      mdiPlus,
      mdiDelete,
      mdiAlert,
      discussions: [],
      votingConfigurations: [],
      showActiveVotingDialog: false,
      activeVotingConfig: null,
      showResultsDialog: false,
      selectedConfig: null,
      userVotes: {} // Para armazenar os votos do usuário atual
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      await this.$services.project.findById(this.$route.params.id)
      
      // Carregar informações do membro atual
      await this.$store.dispatch('projects/setCurrentMember', {
        projectId: this.$route.params.id,
        $repositories: this.$repositories
      })
      
      // Fetch discussions to check their status
      const discussionsRes = await this.$axios.get(`/v1/projects/${this.$route.params.id}/discussions/`)
      this.discussions = Array.isArray(discussionsRes.data?.results) ? discussionsRes.data.results : []
      
      // Load voting configurations from localStorage
      const savedConfigs = localStorage.getItem(`voting_configs_${this.$route.params.id}`)
      if (savedConfigs) {
        this.votingConfigurations = JSON.parse(savedConfigs)
      }

      // Load user votes from localStorage - MANTENDO A REATIVIDADE
      const savedVotes = localStorage.getItem(`user_votes_${this.$route.params.id}_${this.currentUserId}`)
      if (savedVotes) {
        const parsedVotes = JSON.parse(savedVotes)
        // Limpar o objeto atual e adicionar os votos um por um para manter reatividade
        Object.keys(this.userVotes).forEach(key => {
          this.$delete(this.userVotes, key)
        })
        Object.keys(parsedVotes).forEach(key => {
          this.$set(this.userVotes, key, parsedVotes[key])
        })
      }
    } catch(e) {
      throw new Error(e.response.data.detail)
    } finally {
      this.isLoading = false
    }
  },

  head() {
    return {
      title: 'Voting'
    }
  },

  computed: {
    project() {
      return this.$store.getters['projects/project']
    },
    
    isProjectAdmin() {
      return this.$store.getters['projects/isProjectAdmin']
    },

    currentUserId() {
      return this.$store.getters['auth/getUserId']
    },

    // Computed property para garantir reatividade dos votos
    reactiveUserVotes() {
      return this.userVotes
    },

    openDiscussions() {
      const todayString = new Date().toISOString().substr(0, 10)
      return this.discussions.filter(d => 
        d.start_date <= todayString && d.end_date > todayString
      )
    },

    hasDiscussions() {
      return this.discussions.length > 0
    },

    canConfigureVoting() {
      // Button is enabled only if:
      // 1. There are discussions created AND
      // 2. No discussions are currently open (all are closed)
      return this.hasDiscussions && this.openDiscussions.length === 0
    },

    activeVotingForUsers() {
      const now = new Date()
      const currentDate = now.toISOString().substr(0, 10)
      const currentTime = now.toTimeString().substr(0, 5)

      return this.votingConfigurations.filter(config => {
        const startDate = config.startDate
        const endDate = config.endDate
        const startTime = config.startTime
        const endTime = config.endTime

        // Check if current date is within the voting period
        if (currentDate < startDate || currentDate > endDate) {
          return false
        }

        // If it's the start date, check if current time is after start time
        if (currentDate === startDate && currentTime < startTime) {
          return false
        }

        // If it's the end date, check if current time is before end time
        if (currentDate === endDate && currentTime >= endTime) {
          return false
        }

        return true
      })
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

  methods: {
    goToConfiguration() {
      // Check if there's an active voting configuration
      const activeVoting = this.getActiveVotingConfiguration()
      
      if (activeVoting) {
        this.activeVotingConfig = activeVoting
        this.showActiveVotingDialog = true
      } else {
        this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting/configure`))
      }
    },

    getActiveVotingConfiguration() {
      const now = new Date()
      const currentDate = now.toISOString().substr(0, 10)
      const currentTime = now.toTimeString().substr(0, 5)

      return this.votingConfigurations.find(config => {
        const startDate = config.startDate
        const endDate = config.endDate
        const startTime = config.startTime
        const endTime = config.endTime

        // Check if current date is within the voting period
        if (currentDate < startDate || currentDate > endDate) {
          return false
        }

        // If it's the start date, check if current time is after start time
        if (currentDate === startDate && currentTime < startTime) {
          return false
        }

        // If it's the end date, check if current time is before end time
        if (currentDate === endDate && currentTime >= endTime) {
          return false
        }

        return true
      })
    },

    cancelNewVoting() {
      this.showActiveVotingDialog = false
      this.activeVotingConfig = null
    },

    terminateAndCreateNew() {
      if (this.activeVotingConfig) {
        // Find the index of the active voting configuration
        const configIndex = this.votingConfigurations.findIndex(
          config => config.id === this.activeVotingConfig.id
        )

        if (configIndex !== -1) {
          // Terminate the active voting by setting end date and time to now
          const now = new Date()
          this.votingConfigurations[configIndex].endDate = now.toISOString().substr(0, 10)
          this.votingConfigurations[configIndex].endTime = now.toTimeString().substr(0, 5)
          
          // Save to localStorage
          localStorage.setItem(
            `voting_configs_${this.$route.params.id}`, 
            JSON.stringify(this.votingConfigurations)
          )
        }
      }

      // Close dialog and navigate to configuration
      this.showActiveVotingDialog = false
      this.activeVotingConfig = null
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting/configure`))
    },

    editConfiguration(config) {
      // Store the configuration ID to edit in session storage
      sessionStorage.setItem('editingConfigId', config.id.toString())
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/voting/configure`))
    },

    async deleteConfiguration(config, index) {
      const confirmed = await this.$confirm(`Tem certeza de que deseja excluir a configuração de votação "${config.name}"?`, {
        title: 'Excluir Configuração',
        buttonTrueText: 'Excluir',
        buttonFalseText: 'Cancelar',
        color: 'error'
      })

      if (confirmed) {
        this.votingConfigurations.splice(index, 1)
        localStorage.setItem(`voting_configs_${this.$route.params.id}`, JSON.stringify(this.votingConfigurations))
        
        // Also clean up votes for this configuration
        const voteKey = `voting_results_${this.$route.params.id}_${config.id}`
        localStorage.removeItem(voteKey)
      }
    },

    goToDiscussions() {
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/discussions`))
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },

    formatDateTime(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('pt-BR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getVotingMethodText(method) {
      const methods = {
        'approve_only': 'Apenas Aprovar',
        'disapprove_only': 'Apenas Reprovar',
        'approve_disapprove': 'Aprovar ou Reprovar'
      }
      return methods[method] || method
    },

    getVotingMethodColor(method) {
      const colors = {
        'approve_only': 'success',
        'disapprove_only': 'error',
        'approve_disapprove': 'primary'
      }
      return colors[method] || 'grey'
    },

    getVotingMethodDescription(method) {
      const descriptions = {
        'approve_only': 'Anotadores podem apenas aprovar regras que apoiam',
        'disapprove_only': 'Anotadores podem apenas reprovar regras que se opõem',
        'approve_disapprove': 'Anotadores devem votar em todas as regras'
      }
      return descriptions[method] || ''
    },

    getVotingStatusText(config) {
      const results = this.getVotingResults(config.id)
      if (results && Object.keys(results).length > 0) {
        return 'Resultados Disponíveis'
      }
      
      const now = new Date()
      const currentDate = now.toISOString().substr(0, 10)
      const currentTime = now.toTimeString().substr(0, 5)
      
      if (currentDate < config.startDate || (currentDate === config.startDate && currentTime < config.startTime)) {
        return 'Aguardando Início'
      } else if (currentDate > config.endDate || (currentDate === config.endDate && currentTime >= config.endTime)) {
        return 'Encerrada'
      } else {
        return 'Em Andamento'
      }
    },

    getVotingStatusColor(config) {
      const results = this.getVotingResults(config.id)
      if (results && Object.keys(results).length > 0) {
        return 'info'
      }
      
      const now = new Date()
      const currentDate = now.toISOString().substr(0, 10)
      const currentTime = now.toTimeString().substr(0, 5)
      
      if (currentDate < config.startDate || (currentDate === config.startDate && currentTime < config.startTime)) {
        return 'warning'
      } else if (currentDate > config.endDate || (currentDate === config.endDate && currentTime >= config.endTime)) {
        return 'grey'
      } else {
        return 'success'
      }
    },

    getVotingResults(configId) {
      // Get voting results from localStorage
      const resultsKey = `voting_results_${this.$route.params.id}_${configId}`
      const results = localStorage.getItem(resultsKey)
      return results ? JSON.parse(results) : null
    },

    getRuleVotes(configId, ruleIndex, voteType) {
      const results = this.getVotingResults(configId)
      if (!results || !results[ruleIndex]) {
        return 0
      }

      const ruleVotes = results[ruleIndex]
      switch (voteType) {
        case 'approve':
          return Object.values(ruleVotes).filter(vote => vote === 'approve').length
        case 'disapprove':
          return Object.values(ruleVotes).filter(vote => vote === 'disapprove').length
        case 'neutral':
          return Object.values(ruleVotes).filter(vote => !vote || vote === 'neutral').length
        default:
          return 0
      }
    },

    getRuleApprovalPercentage(configId, ruleIndex) {
      const results = this.getVotingResults(configId)
      if (!results || !results[ruleIndex]) {
        return 0
      }

      const ruleVotes = results[ruleIndex]
      const totalVotes = Object.keys(ruleVotes).length
      if (totalVotes === 0) return 0

      const approvals = Object.values(ruleVotes).filter(vote => vote === 'approve').length
      return (approvals / totalVotes) * 100
    },

    getTotalParticipants(configId) {
      const results = this.getVotingResults(configId)
      if (!results) {
        return 0
      }

      // Get unique user IDs across all rules
      const allUserIds = new Set()
      Object.values(results).forEach(ruleVotes => {
        Object.keys(ruleVotes).forEach(userId => {
          allUserIds.add(userId)
        })
      })
      
      return allUserIds.size
    },

    getUserVote(configId, ruleIndex) {
      const voteKey = `${configId}_${ruleIndex}`
      // Forçar reatividade retornando diretamente do objeto reativo
      return this.userVotes[voteKey] || null
    },

    vote(configId, ruleIndex, vote) {
      const voteKey = `${configId}_${ruleIndex}`
      const previousVote = this.userVotes[voteKey]
      
      // Update user votes immediately
      if (vote === null) {
        this.$delete(this.userVotes, voteKey)
      } else {
        this.$set(this.userVotes, voteKey, vote)
      }
      
      // Force Vue to update the DOM
      this.$forceUpdate()
      
      // Save user votes to localStorage
      localStorage.setItem(
        `user_votes_${this.$route.params.id}_${this.currentUserId}`,
        JSON.stringify(this.userVotes)
      )
      
      // Update voting results
      this.updateVotingResults(configId, ruleIndex, vote)
      
      // Show enhanced confirmation with better messaging
      let message = ''
      let color = 'success'
      
      if (vote === null) {
        message = 'Voto removido com sucesso!'
        color = 'info'
      } else if (previousVote && previousVote !== vote) {
        message = `Voto alterado para: ${vote === 'approve' ? 'APROVADO ✓' : 'REPROVADO ✗'}`
        color = vote === 'approve' ? 'success' : 'warning'
      } else if (!previousVote) {
        message = `Voto registrado: ${vote === 'approve' ? 'APROVADO ✓' : 'REPROVADO ✗'}`
        color = vote === 'approve' ? 'success' : 'error'
      }
      
      // Small delay to ensure visual update happens first
      this.$nextTick(() => {
        this.$store.dispatch('notification/setNotification', {
          color,
          text: message,
          timeout: 4000
        })
      })
    },

    updateVotingResults(configId, ruleIndex, vote) {
      const resultsKey = `voting_results_${this.$route.params.id}_${configId}`
      const results = this.getVotingResults(configId) || {}
      
      // Initialize rule if it doesn't exist
      if (!results[ruleIndex]) {
        results[ruleIndex] = {}
      }
      
      // Update or remove user's vote
      if (vote === null) {
        delete results[ruleIndex][this.currentUserId]
      } else {
        results[ruleIndex][this.currentUserId] = vote
      }
      
      // Save results to localStorage
      localStorage.setItem(resultsKey, JSON.stringify(results))
    },

    viewDetailedResults(config) {
      this.selectedConfig = config
      this.showResultsDialog = true
    }
  }
}
</script>

<style scoped>
/* Transições suaves para os botões de votação */
.v-btn {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

/* Efeito hover melhorado */
.v-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
}

/* Animação para alertas de status */
.v-alert {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Estilo especial para botões selecionados */
.v-btn:not(.v-btn--outlined) {
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16) !important;
}

/* Pulse animation para chips de status */
.v-chip {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
  }
}

/* Estilo para cards de regras com hover */
.v-card {
  transition: all 0.3s ease !important;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
}

/* Estilos específicos para os botões de votação */
.vote-button {
  min-width: 100px !important;
  font-weight: bold !important;
  border-width: 2px !important;
}

/* Botão aprovado - verde */
.vote-approve {
  background-color: #4CAF50 !important;
  border-color: #4CAF50 !important;
  color: white !important;
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3) !important;
}

.vote-approve:hover {
  background-color: #45a049 !important;
  box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4) !important;
}

/* Botão reprovado - vermelho */
.vote-disapprove {
  background-color: #f44336 !important;
  border-color: #f44336 !important;
  color: white !important;
  box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3) !important;
}

.vote-disapprove:hover {
  background-color: #da190b !important;
  box-shadow: 0 6px 12px rgba(244, 67, 54, 0.4) !important;
}

/* Botões selecionados têm borda mais grossa */
.vote-selected {
  border-width: 3px !important;
  transform: scale(1.05) !important;
}

/* Remover outline padrão dos botões */
.vote-button .v-btn__content {
  font-weight: bold !important;
  letter-spacing: 0.5px !important;
}

/* Animação de clique */
.vote-button:active {
  transform: scale(0.95) !important;
}
</style> 