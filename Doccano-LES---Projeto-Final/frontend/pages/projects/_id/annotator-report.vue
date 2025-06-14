<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex align-center mb-6">
          <v-btn icon class="mr-4" @click="$router.back()">
            <v-icon>{{ mdiArrowLeft }}</v-icon>
          </v-btn>
          <h1 class="text-h4">Relatório de Anotadores</h1>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-tabs v-model="activeTab" grow>
          <v-tab>Progresso Individual</v-tab>
          <v-tab>Desempenho da Equipe</v-tab>
          <v-tab>Informações Gerais</v-tab>
        </v-tabs>

        <v-tabs-items v-model="activeTab">
          <!-- Progresso Individual -->
          <v-tab-item>
            <v-card flat class="mt-4">
              <v-card-text>
                <h3 class="mb-3">Progresso de Anotação por Anotador</h3>
                
                <v-skeleton-loader
                  v-if="isLoading"
                  type="list-item-three-line@5"
                ></v-skeleton-loader>
                
                <div v-else>
                  <div v-for="(item, index) in memberProgress.progress" :key="index" class="mb-4">
                    <div class="d-flex justify-space-between align-center mb-1">
                      <div>
                        <v-avatar size="32" color="primary" class="white--text mr-2">
                          {{ getInitials(item.user) }}
                        </v-avatar>
                        <span class="font-weight-medium">{{ item.user }}</span>
                      </div>
                      <div>
                        <span class="font-weight-medium">{{ item.done }} / {{ memberProgress.total }}</span>
                        <span class="ml-2 grey--text">({{ calculatePercentage(item.done, memberProgress.total) }}%)</span>
                      </div>
                    </div>
                    <v-progress-linear 
                      :value="calculatePercentage(item.done, memberProgress.total)" 
                      height="12"
                      :color="getProgressColor(calculatePercentage(item.done, memberProgress.total))"
                    ></v-progress-linear>
                  </div>

                  <v-alert 
                    v-if="memberProgress.progress && memberProgress.progress.length === 0"
                    type="info"
                    class="mt-4"
                  >
                    Nenhum dado de progresso de anotadores disponível.
                  </v-alert>
                </div>
              </v-card-text>
            </v-card>
          </v-tab-item>

          <!-- Desempenho da Equipe -->
          <v-tab-item>
            <v-card flat class="mt-4">
              <v-card-text>
                <h3 class="mb-3">Desempenho da Equipe</h3>
                
                <v-skeleton-loader
                  v-if="isLoading"
                  type="table"
                ></v-skeleton-loader>
                
                <div v-else>
                  <v-simple-table>
                    <template #default>
                      <thead>
                        <tr>
                          <th class="text-left">Métrica</th>
                          <th class="text-left">Valor</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>Total de anotadores</td>
                          <td>{{ annotators.length }}</td>
                        </tr>
                        <tr>
                          <td>Anotações concluídas (total)</td>
                          <td>{{ getTotalAnnotationsDone() }}</td>
                        </tr>
                        <tr>
                          <td>Total de itens no projeto</td>
                          <td>{{ memberProgress.total }}</td>
                        </tr>
                        <tr>
                          <td>Progresso geral</td>
                          <td>
                            {{ calculateTeamProgress() }}%
                            <v-progress-linear 
                              :value="calculateTeamProgress()" 
                              class="mt-1"
                              :color="getProgressColor(calculateTeamProgress())"
                            ></v-progress-linear>
                          </td>
                        </tr>
                        <tr>
                          <td>Média de anotações por anotador</td>
                          <td>{{ calculateAverageAnnotationsPerAnnotator() }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </div>
              </v-card-text>
            </v-card>
          </v-tab-item>

          <!-- Informações Gerais -->
          <v-tab-item>
            <v-card flat class="mt-4">
              <v-card-text>
                <h3 class="mb-3">Lista de Anotadores</h3>
                
                <v-skeleton-loader
                  v-if="isLoading"
                  type="list-item-avatar-three-line@5"
                ></v-skeleton-loader>
                
                <div v-else>
                  <v-list two-line>
                    <v-list-item v-for="(member, index) in annotators" :key="index">
                      <v-list-item-avatar color="primary">
                        <span class="white--text">{{ getInitials(member.username) }}</span>
                      </v-list-item-avatar>
                      <v-list-item-content>
                        <v-list-item-title>{{ member.username }}</v-list-item-title>
                        <v-list-item-subtitle>ID: {{ member.id }}, User ID: {{ member.user }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>

                  <v-alert 
                    v-if="annotators.length === 0"
                    type="info"
                    class="mt-4"
                  >
                    Nenhum anotador encontrado para este projeto.
                  </v-alert>
                </div>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mdiArrowLeft } from '@mdi/js'

export default {
  layout: 'project',
  data() {
    return {
      mdiArrowLeft,
      activeTab: 0,
      isLoading: false,
      annotators: [],
      memberProgress: {
        total: 0,
        progress: []
      }
    }
  },
  computed: {
    projectId() {
      return this.$route.params.id
    }
  },
  async created() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.isLoading = true
      
      try {
        // Carrega os membros (filtrando apenas anotadores)
        const members = await this.$repositories.member.list(this.projectId)
        this.annotators = members.filter(member => member.rolename === 'annotator')
        
        // Carrega dados de progresso dos anotadores
        this.memberProgress = await this.$repositories.metrics.fetchMemberProgress(this.projectId)
        
      } catch (error) {
        console.error('Erro ao carregar dados de anotadores:', error)
        this.$toast.error('Erro ao carregar dados do relatório')
      } finally {
        this.isLoading = false
      }
    },
    getInitials(name) {
      if (!name) return 'A'
      return name
        .split(' ')
        .map(part => part.charAt(0).toUpperCase())
        .slice(0, 2)
        .join('')
    },
    calculatePercentage(done, total) {
      if (total === 0) return 0
      return Math.round((done / total) * 100)
    },
    getProgressColor(percentage) {
      if (percentage < 30) return 'red'
      if (percentage < 70) return 'orange'
      return 'green'
    },
    getTotalAnnotationsDone() {
      if (!this.memberProgress.progress) return 0
      return this.memberProgress.progress.reduce((total, item) => total + item.done, 0)
    },
    calculateTeamProgress() {
      if (this.memberProgress.total === 0 || !this.memberProgress.progress) return 0
      const totalAnnotations = this.getTotalAnnotationsDone()
      const totalExpected = this.memberProgress.total * Math.max(1, this.annotators.length)
      return Math.round((totalAnnotations / totalExpected) * 100)
    },
    calculateAverageAnnotationsPerAnnotator() {
      if (this.annotators.length === 0 || !this.memberProgress.progress) return 0
      const totalAnnotations = this.getTotalAnnotationsDone()
      return Math.round(totalAnnotations / this.annotators.length)
    }
  }
}
</script> 