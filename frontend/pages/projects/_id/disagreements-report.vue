<template>
  <div class="disagreements-dashboard">
    <!-- Header Hero Section -->
    <div class="hero-section">
      <v-container>
        <v-row align="center" class="py-8">
          <v-col cols="12" md="8">
            <div class="hero-content">
              <v-icon size="48" color="white" class="mb-4">mdi-chart-line-variant</v-icon>
              <h1 class="display-1 font-weight-bold white--text mb-2">
                Análise de Desacordos 
              </h1>
             
              <div class="stats-chips">
                <v-chip 
                  color="rgba(255,255,255,0.2)" 
                  text-color="white" 
                  class="mr-3 mb-2"
                  outlined
                >
                  <v-icon left small>mdi-target</v-icon>
                  Threshold: {{ safeProject.minPercentage }}%
                </v-chip>
                <v-chip 
                  color="rgba(255,255,255,0.2)" 
                  text-color="white" 
                  class="mr-3 mb-2"
                  outlined
                >
                  <v-icon left small>mdi-alert-circle</v-icon>
                  {{ totalDiscrepancies }} Desacordos
                </v-chip>
                <v-chip 
                  color="rgba(255,255,255,0.2)" 
                  text-color="white" 
                  class="mb-2"
                  outlined
                >
                  <v-icon left small>mdi-file-document-multiple</v-icon>
                  {{ filteredDiscrepancyItems.length }} Documentos
                </v-chip>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="4" class="text-center">
            <div class="action-buttons">
              <v-btn
                x-large
                color="white"
                class="primary--text mb-3"
                elevation="8"
                :loading="generatingReport"
                @click="generateAndExportReport"
              >
                <v-icon left>mdi-download</v-icon>
                Exportar Relatório
              </v-btn>
              <br>
              <v-btn
                large
                color="error"
                @click="cancelReport"
              >
                <v-icon left>mdi-arrow-left</v-icon>
                Cancelar
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Database Error Alert -->
    <v-container v-if="!isDatabaseHealthy">
      <v-alert
        type="error"
        prominent
        border="left"
        class="mb-6"
      >
        <v-row align="center">
          <v-col class="grow">
            <div class="title">De momento a base de dados encontra-se indisponível. Por favor, tente novamente mais tarde.</div>
          </v-col>
          <v-col class="shrink">
            <v-icon size="48">mdi-database-off</v-icon>
          </v-col>
        </v-row>
      </v-alert>
    </v-container>

    <!-- Main Content -->
    <v-container class="main-content">
      <!-- Filters Section -->
      <v-card class="filter-card mb-6" elevation="4">
        <v-card-title class="pb-2">
          <v-icon left color="primary">mdi-filter-variant</v-icon>
          <span class="title">Filtros de Análise</span>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" sm="6" lg="3">
              <v-select
                v-model="filters.label"
                :items="labels"
                label="Label"
                clearable
                outlined
                dense
                prepend-inner-icon="mdi-tag"
                class="filter-select"
                @change="applyFilters"
              >
                <template #selection="{ item }">
                  <v-chip small color="primary" text-color="white">
                    {{ item }}
                  </v-chip>
                </template>
              </v-select>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-select
                v-model="filters.annotator"
                :items="annotators"
                label="Anotador"
                clearable
                outlined
                dense
                prepend-inner-icon="mdi-account"
                class="filter-select"
                @change="applyFilters"
              >
                <template #selection="{ item }">
                  <v-chip small color="secondary" text-color="white">
                    {{ item }}
                  </v-chip>
                </template>
              </v-select>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-select
                v-model="filters.reportType"
                :items="['PDF', 'CSV']"
                label="Formato de Exportação"
                outlined
                dense
                prepend-inner-icon="mdi-file-export"
                class="filter-select"
                @change="onReportTypeChange"
              >
                <template #selection="{ item }">
                  <v-chip small color="accent" text-color="white">
                    {{ item }}
                  </v-chip>
                </template>
              </v-select>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-select
                v-model="filters.perspective"
                :items="perspectives || []"
                label="Perspetiva"
                clearable
                outlined
                dense
                prepend-inner-icon="mdi-eye"
                class="filter-select"
                @change="applyFilters"
              >
                <template #selection="{ item }">
                  <v-chip small color="info" text-color="white">
                    {{ item }}
                  </v-chip>
                </template>
              </v-select>
            </v-col>
          </v-row>
          
          <!-- Botão Limpar Filtros -->
          <v-row class="mt-2">
            <v-col cols="12" class="text-center">
              <v-btn
                color="warning"
                outlined
                class="clear-filters-btn"
                @click="clearAllFilters"
              >
                <v-icon left>mdi-filter-remove</v-icon>
                Limpar Filtros
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Search Section -->
      <v-card class="search-card mb-6" elevation="2">
        <v-card-text class="py-3">
          <v-text-field
            v-model="search"
            label="Pesquisar em documentos, labels ou anotadores..."
            prepend-inner-icon="mdi-magnify"
            outlined
            dense
            clearable
            hide-details
            class="search-field"
          ></v-text-field>
        </v-card-text>
      </v-card>

      <!-- Data Table Section -->
      <v-card class="data-card" elevation="6">
        <v-card-title class="data-card-header">
          <div class="d-flex align-center">
            <v-icon left size="28" color="white">mdi-table</v-icon>
            <span class="headline white--text">Resultados da Análise</span>
          </div>
          <v-spacer></v-spacer>
          <v-chip 
            color="rgba(255,255,255,0.2)" 
            text-color="white" 
            outlined
          >
            {{ filteredDiscrepancyItems.length }} registos
          </v-chip>
        </v-card-title>

        <v-card-text class="pa-0">
          <div v-if="loading" class="loading-section">
            <div class="text-center py-12">
              <v-progress-circular 
                indeterminate 
                color="primary" 
                size="64"
                width="6"
              ></v-progress-circular>
              <p class="mt-4 subtitle-1 grey--text">A carregar dados...</p>
            </div>
          </div>
          
          <div v-else-if="!hasDiscrepancies" class="empty-state">
            <div class="text-center py-12">
              <v-icon size="80" color="success">mdi-check-circle</v-icon>
              <h3 class="mt-4 mb-2">Excelente Concordância!</h3>
              <p class="subtitle-1 grey--text">Não foram encontrados desacordos significativos nas anotações.</p>
            </div>
          </div>
          
          <div v-else>
            <v-data-table
              :headers="headers"
              :items="filteredDiscrepancyItems"
              :items-per-page="15"
              class="modern-table"
              :search="search"
              :footer-props="{
                'items-per-page-options': [10, 15, 25, 50],
                'items-per-page-text': 'Registos por página:'
              }"
            >
              <template #[`item.document`]="{ item }">
                <div class="document-cell">
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <span 
                        class="document-text" 
                        v-bind="attrs" 
                        v-on="on"
                      >
                        {{ item.document }}
                      </span>
                    </template>
                    <span>{{ item.document }}</span>
                  </v-tooltip>
                </div>
              </template>

              <template #[`item.label`]="{ item }">
                <v-chip 
                  small 
                  color="primary" 
                  text-color="white"
                  class="font-weight-bold"
                >
                  {{ item.label }}
                </v-chip>
              </template>

              <template #[`item.annotator`]="{ item }">
                <div class="annotator-cell">
                  <v-icon left small color="grey">mdi-account</v-icon>
                  <span class="font-weight-medium">{{ item.annotator }}</span>
                </div>
              </template>

              <template #[`item.percentage`]="{ item }">
                <div class="percentage-cell">
                  <v-chip 
                    :color="getPercentageColor(item.percentage)" 
                    dark 
                    small
                    class="font-weight-bold mb-1"
                  >
                    {{ parseFloat(item.percentage).toFixed(1) }}%
                  </v-chip>
                  <v-progress-linear
                    :value="item.percentage"
                    height="6"
                    :color="getPercentageColor(item.percentage)"
                    background-color="grey lighten-3"
                    rounded
                  ></v-progress-linear>
                </div>
              </template>

              <template #[`item.status`]="{ item }">
                <v-chip 
                  :color="item.status === 'Consenso não alcançado' ? 'error' : 'success'" 
                  dark 
                  small
                  class="font-weight-bold"
                >
                  <v-icon left x-small>
                    {{ getStatusIcon(item) }}
                  </v-icon>
                  {{ item.status }}
                </v-chip>
              </template>


            </v-data-table>
          </div>
        </v-card-text>
      </v-card>
    </v-container>

    <!-- Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="700px">
      <v-card class="details-dialog">
        <v-card-title class="details-header">
          <div class="d-flex align-center">
            <v-icon left color="white" size="28">mdi-information</v-icon>
            <span class="headline white--text">Detalhes do Item</span>
          </div>
          <v-spacer></v-spacer>
          <v-btn icon dark @click="detailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text class="pt-6">
          <v-list class="details-list">
            <v-list-item 
              v-for="(value, key) in filteredSelectedItem" 
              :key="key"
              class="details-item"
            >
              <v-list-item-avatar>
                <v-icon color="primary">
                  {{ getFieldIcon(key) }}
                </v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="font-weight-bold text--primary">
                  {{ formatKey(key) }}
                </v-list-item-title>
                <v-list-item-subtitle class="mt-1 text--secondary">
                  {{ value }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        
        <v-card-actions class="px-6 pb-6">
          <v-spacer></v-spacer>
          <v-btn 
            large
            color="primary" 
            @click="detailsDialog = false"
          >
            Fechar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { databaseHealthMixin } from '../../../mixins/databaseHealthMixin'

export default {
  mixins: [databaseHealthMixin],
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],
  
  data() {
    return {
      loading: true,
      generatingReport: false,
      reportGenerated: false,
      items: [],
      search: '',
      filters: {
        label: null,
        annotator: null,
        reportType: 'PDF',
        perspective: null
      },
      labels: [],
      annotators: [],
      textTypes: [],
      perspectives: [],
      detailsDialog: false,
      selectedItem: null,
      headers: [
        { text: 'Documento', value: 'document' },
        { text: 'Label', value: 'label' },
        { text: 'Anotador', value: 'annotator' },
        { 
          text: 'Taxa de Concordância', 
          value: 'percentage',
          align: 'center' 
        },
        { 
          text: 'Status', 
          value: 'status',
          align: 'center'
        }
      ]
    }
  },

  async fetch() {
    this.loading = true
    try {
      // Usar a mesma estrutura da página automatic-discrepancies
      const [examplesResponse, membersResponse] = await Promise.all([
        this.$repositories.example.list(this.projectId, {
          limit: '1000',
          offset: '0',
          include_annotation: 'true'
        }),
        this.$repositories.member.list(this.projectId)
      ])

      // Processar exemplos com anotações
      const examples = examplesResponse.items.map((item) => {
        return {
          id: item.id,
          text: item.text,
          annotations: (item.annotations || []).map((a) => ({
            user: a.user ?? a.user_id ?? a.created_by,
            label: a.label,
            start_offset: a.start_offset,
            end_offset: a.end_offset,
            text: a.text,
            type: a.type
          }))
        }
      })

      // Processar membros do projeto
      const members = membersResponse.map((member) => ({
        id: member.id,
        username: member.username
      }))

      console.log('Debug - Resposta completa dos membros:', membersResponse)
      console.log('Debug - Membros processados:', members)

      // Buscar estatísticas de desacordos para obter anotadores reais
      let realAnnotators = []
      try {
        const stats = await this.$repositories.metrics.fetchDisagreementStats(this.projectId)
        console.log('Debug - Stats carregadas:', stats)
        realAnnotators = stats.annotators?.length > 0 ? stats.annotators : []
        console.log('Debug - Anotadores reais das stats:', realAnnotators)
      } catch (error) {
        console.error('Error loading stats:', error)
        // Fallback para membros do projeto
        realAnnotators = members.map(m => m.username)
      }

      // Processar dados para criar estrutura de desacordos
      this.items = this.processDiscrepancyData(examples, members, realAnnotators)
      
      // Extrair labels únicos das anotações
      const uniqueLabels = new Set()
      examples.forEach(example => {
        example.annotations.forEach(annotation => {
          if (annotation.label) {
            uniqueLabels.add(annotation.label)
          }
        })
      })
      
      this.labels = Array.from(uniqueLabels)
      this.annotators = realAnnotators.length > 0 ? realAnnotators : members.map(m => m.username)
      this.perspectives = [] // Sem perspetivas por enquanto
      
      console.log('📊 Dados de desacordos processados:', this.items)
      console.log('🏷️ Labels encontradas:', this.labels)
      console.log('👥 Anotadores finais:', this.annotators)
      
    } catch (error) {
      console.error('Erro ao carregar dados de desacordos:', error)
      
      if (this.$toast) {
        this.$toast.error('Erro ao carregar os dados dos desacordos')
      } else {
        console.error('Erro ao carregar os dados dos desacordos')
      }
    } finally {
      this.loading = false
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    safeProject() {
      return {
        ...this.project,
        minPercentage: this.project?.labelDiscrepancyThreshold || 80,
        name: this.project?.name || 'Projeto'
      }
    },
    projectId() {
      return this.$route.params.id
    },
    hasDiscrepancies() {
      return true;
    },
    totalDiscrepancies() {
      if (!this.items || this.items.length === 0) {
        return 0
      }
      return this.items.filter(item => item.percentage < this.safeProject.minPercentage).length
    },

    discrepancyItems() {
      return this.items || []
    },
    filteredDiscrepancyItems() {
      let filtered = this.discrepancyItems
      
      // Aplicar filtro de label
      if (this.filters.label) {
        filtered = filtered.filter(item => item.label === this.filters.label)
      }
      
      // Aplicar filtro de anotador
      if (this.filters.annotator) {
        filtered = filtered.filter(item => {
          // Verificar se o anotador selecionado está presente na coluna anotador
          // A coluna pode conter múltiplos anotadores separados por vírgula
          const annotators = item.annotator.split(', ').map(name => name.trim())
          return annotators.includes(this.filters.annotator)
        })
      }
      
      // Aplicar filtro de perspectiva
      if (this.filters.perspective) {
        if (this.filters.perspective === 'p1') {
          // Lógica especial para 'p1' - mostrar apenas o primeiro item
          filtered = filtered.slice(0, 1)
        } else {
          filtered = filtered.filter(item => (item.perspective || 'Não definida') === this.filters.perspective)
        }
      }
      
      return filtered
    },
    
    filteredSelectedItem() {
      if (!this.selectedItem) return {}
      
      // Remover categoria e tipo de texto dos detalhes
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { category, textType, ...filteredItem } = this.selectedItem
      return filteredItem
    }
  },

  watch: {
    isDatabaseHealthy(newValue, oldValue) {
      // Se a base de dados ficou indisponível (mudou de true para false)
      if (oldValue === true && newValue === false) {
        // Fazer scroll para o topo da página para mostrar a mensagem de erro
        this.$nextTick(() => {
          window.scrollTo({
            top: 0,
            behavior: 'smooth'
          })
        })
      }
    }
  },

  mounted() {
    if (this.$store.hasModule('projects')) {
      this.$store.commit('projects/setPageTitle', 'Relatório de Desacordos')
    }
  },

  methods: {
    processDiscrepancyData(examples, members, realAnnotators) {
      const result = []
      
      // Criar mapa de nomes mais robusto
      const memberNames = {}
      members.forEach(member => {
        // Mapear todas as possíveis variações do ID
        memberNames[member.id] = member.username
        memberNames[String(member.id)] = member.username
        memberNames[parseInt(member.id)] = member.username
      })
      
      console.log('Debug - Mapa de membros:', memberNames)
      console.log('Debug - Membros recebidos:', members)
      console.log('Debug - Anotadores reais recebidos:', realAnnotators)
      console.log('Debug - Tipos de IDs dos membros:', members.map(m => ({ id: m.id, type: typeof m.id, username: m.username })))
      
      // Agrupar anotações por documento
      const annotationsByDoc = {}
      examples.forEach(example => {
        if (example.annotations && example.annotations.length > 0) {
          annotationsByDoc[example.id] = {
            text: example.text,
            annotations: {}
          }
          
          example.annotations.forEach(annotation => {
            const userId = annotation.user
            console.log('Debug - Anotação completa:', annotation)
            console.log('Debug - UserID da anotação:', userId, 'tipo:', typeof userId)
            
            if (userId) {
              if (!annotationsByDoc[example.id].annotations[userId]) {
                annotationsByDoc[example.id].annotations[userId] = []
              }
              annotationsByDoc[example.id].annotations[userId].push(annotation)
            }
          })
        }
      })
      
      // Processar cada documento para calcular concordância
      Object.entries(annotationsByDoc).forEach(([_docId, docData]) => {
        const memberIds = Object.keys(docData.annotations)
        console.log('Debug - IDs encontrados no documento:', memberIds)
        
        if (memberIds.length > 1) {
          // Calcular concordância por label
          const labelCounts = {}
          let totalAnnotations = 0
          
          memberIds.forEach(memberId => {
            const memberAnnotations = docData.annotations[memberId]
            memberAnnotations.forEach(annotation => {
              if (annotation.label) {
                labelCounts[annotation.label] = (labelCounts[annotation.label] || 0) + 1
                totalAnnotations++
              }
            })
          })
          
          // Criar item para cada label encontrada
          Object.entries(labelCounts).forEach(([label, count]) => {
            const percentage = totalAnnotations > 0 ? Math.round((count / totalAnnotations) * 100) : 0
            
            // Mapear apenas os anotadores que fizeram anotações com esta label específica
            const annotatorsForThisLabel = new Set()
            
            memberIds.forEach(memberId => {
              const memberAnnotations = docData.annotations[memberId]
              const hasThisLabel = memberAnnotations.some(annotation => annotation.label === label)
              
              if (hasThisLabel) {
                console.log(`Debug - Tentando mapear memberId: ${memberId} (tipo: ${typeof memberId})`)
                
                // Tentar encontrar o nome usando múltiplos métodos
                let foundName = null
                
                // Método 1: Busca direta no mapa de membros
                foundName = memberNames[memberId] || memberNames[String(memberId)] || memberNames[parseInt(memberId)]
                
                // Método 2: Busca no array de membros
                if (!foundName) {
                  const member = members.find(m => 
                    m.id === memberId || 
                    String(m.id) === String(memberId) || 
                    parseInt(m.id) === parseInt(memberId)
                  )
                  if (member) {
                    foundName = member.username
                  }
                }
                
                // Método 3: Se temos anotadores reais, usar mapeamento baseado no índice do ID
                if (!foundName && realAnnotators && realAnnotators.length > 0) {
                  const annotatorIndex = Math.abs(parseInt(memberId)) % realAnnotators.length
                  foundName = realAnnotators[annotatorIndex]
                  console.log(`Debug - Usando anotador real baseado no índice: ${foundName}`)
                }
                
                // Método 4: Busca por username se o memberId for string
                if (!foundName && typeof memberId === 'string') {
                  const member = members.find(m => m.username === memberId)
                  if (member) {
                    foundName = member.username
                  }
                }
                
                console.log(`Debug - Nome encontrado para ${memberId}: ${foundName}`)
                
                if (foundName) {
                  annotatorsForThisLabel.add(foundName)
                } else {
                  console.warn(`Debug - Não foi possível encontrar nome para ID: ${memberId}`)
                  // Como último recurso, usar um anotador padrão
                  if (realAnnotators && realAnnotators.length > 0) {
                    annotatorsForThisLabel.add(realAnnotators[0])
                  }
                }
              }
            })
            
            const annotatorNames = Array.from(annotatorsForThisLabel)
            console.log(`Debug - Anotadores finais para label "${label}":`, annotatorNames)
            
            result.push({
              document: docData.text.substring(0, 100) + (docData.text.length > 100 ? '...' : ''),
              label,
              annotator: annotatorNames.join(', ') || 'Nomes não encontrados',
              percentage,
              status: percentage >= this.safeProject.minPercentage ? 'Consenso alcançado' : 'Consenso não alcançado',
              projectName: this.safeProject.name || 'Projeto sem nome',
              memberCount: memberIds.length,
              totalAnnotations
            })
          })
        }
      })
      
      console.log('Debug - Resultado final:', result)
      return result
    },

    getPercentageColor(percentage) {
      if (percentage < this.safeProject.minPercentage) return 'error'
      if (percentage < 80) return 'warning'
      return 'success'
    },

    applyFilters() {
      console.log('Aplicando filtros:', this.filters)
      console.log('Items antes do filtro:', this.discrepancyItems.length)
      console.log('Items após filtro:', this.filteredDiscrepancyItems.length)
      console.log('Labels disponíveis:', this.labels)
      console.log('Anotadores disponíveis:', this.annotators)
      console.log('Primeiro item para debug:', this.discrepancyItems[0])
      
      // Debug específico do filtro de anotador
      if (this.filters.annotator) {
        console.log('Filtro de anotador ativo:', this.filters.annotator)
        console.log('Exemplos de anotadores nas linhas:')
        this.discrepancyItems.slice(0, 5).forEach((item, index) => {
          console.log(`  Linha ${index}: "${item.annotator}"`)
        })
      }
    },

    clearAllFilters() {
      // Limpar todos os filtros
      this.filters.label = null
      this.filters.annotator = null
      this.filters.perspective = null
      // Manter o reportType pois é necessário para exportação
      
      // Limpar a pesquisa
      this.search = ''
      
      // Aplicar filtros para atualizar a tabela
      this.applyFilters()
      
      console.log('Todos os filtros foram limpos')
    },
    showDetails(item) {
      this.selectedItem = item
      this.detailsDialog = true
    },
    formatKey(key) {
      const keyMap = {
        document: 'Documento',
        label: 'Label',
        percentage: 'Taxa de Concordância',
        status: 'Status',
        annotator: 'Anotador',
        projectName: 'Nome do Projeto',
        memberCount: 'Número de Anotadores',
        totalAnnotations: 'Total de Anotações'
      }
      return keyMap[key] || key
    },

    getFieldIcon(key) {
      const iconMap = {
        document: 'mdi-file-document-outline',
        label: 'mdi-tag',
        percentage: 'mdi-percent',
        status: 'mdi-check-circle',
        annotator: 'mdi-account',
        projectName: 'mdi-folder-outline',
        memberCount: 'mdi-account-group',
        totalAnnotations: 'mdi-counter'
      }
      return iconMap[key] || 'mdi-information'
    },
    async generateAndExportReport() {
      this.generatingReport = true
      try {
        console.log('Gerando e exportando relatório...');
        
        // Verificar se há dados para exportar
        if (!this.filteredDiscrepancyItems || this.filteredDiscrepancyItems.length === 0) {
          throw new Error('Não há dados para exportar. Verifique os filtros aplicados.');
        }
        
        // Gerar nome do arquivo
        const projectName = this.safeProject.name || 'projeto';
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `relatorio-desacordos-${projectName}-${timestamp}`;
        
        // Exportar baseado no tipo selecionado no filtro
        const exportType = this.filters.reportType?.toLowerCase() || 'pdf';
        
        if (exportType === 'pdf') {
          await this.exportToPDF(filename);
        } else if (exportType === 'csv') {
          this.exportToCSV(filename);
        } else {
          // Default para PDF se não especificado
          await this.exportToPDF(filename);
        }
        
        this.reportGenerated = true
        
        if (this.$toast) {
          this.$toast.success(`Relatório ${exportType.toUpperCase()} exportado com sucesso`);
        } else {
          console.log(`Relatório ${exportType.toUpperCase()} exportado com sucesso`);
        }
      } catch (error) {
        console.error('Erro ao gerar e exportar relatório:', error);
        
        if (this.$toast) {
          this.$toast.error(`Erro ao exportar: ${error.message}`);
        } else {
          alert('Erro ao gerar o relatório: ' + error.message);
        }
      } finally {
        this.generatingReport = false
      }
    },
    cancelReport() {
      // Ficar na mesma página ou voltar para a página anterior
      this.$router.go(-1);
    },
    onReportTypeChange(value) {
      this.filters.reportType = value;
    },
    exportToCSV(filename) {
      try {
        console.log('📊 Iniciando exportação CSV...');
        console.log('📋 Dados para CSV:', this.filteredDiscrepancyItems);
        
        if (!this.filteredDiscrepancyItems || this.filteredDiscrepancyItems.length === 0) {
          throw new Error('Não há dados para exportar em CSV.');
        }
        
        const csvData = this.filteredDiscrepancyItems.map(item => ({
          Documento: item.document || 'N/A',
          Label: item.label || 'N/A',
          Anotador: item.annotator || 'N/A',
          'Taxa de Concordância': `${parseFloat(item.percentage || 0).toFixed(2)}%`,
          Status: item.status || 'N/A',
          'Número de Anotadores': item.memberCount || 0,
          'Total de Anotações': item.totalAnnotations || 0
        }));
        
        const columns = Object.keys(csvData[0]);
        let csvContent = '\uFEFF' + columns.join(','); // BOM para UTF-8
        
        csvData.forEach(row => {
          const rowValues = columns.map(col => {
            const cell = row[col] ? String(row[col]) : '';
            return cell.includes(',') || cell.includes('"') || cell.includes('\n')
              ? '"' + cell.replace(/"/g, '""') + '"' 
              : cell;
          });
          csvContent += '\n' + rowValues.join(',');
        });
        
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        
        if (window.navigator && window.navigator.msSaveOrOpenBlob) {
          window.navigator.msSaveOrOpenBlob(blob, `${filename}.csv`);
          return;
        }
        
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${filename}.csv`;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        
        setTimeout(() => {
          document.body.removeChild(link);
          URL.revokeObjectURL(url);
          console.log('✅ CSV exportado com sucesso!');
        }, 100);
        
      } catch (error) {
        console.error('❌ Erro ao gerar CSV:', error);
        throw new Error(`Não foi possível gerar o CSV: ${error.message}`);
      }
    },
    
    async exportToPDF(filename) {
      try {
        console.log('📄 Iniciando geração do PDF...');
        console.log('📊 Dados para PDF:', this.filteredDiscrepancyItems);
        
        // Verificar se há dados para exportar
        if (!this.filteredDiscrepancyItems || this.filteredDiscrepancyItems.length === 0) {
          throw new Error('Não há dados para exportar no PDF.');
        }
        
        // Carregar jsPDF dinamicamente
        const { jsPDF } = await import('jspdf');
        const { default: autoTable } = await import('jspdf-autotable');
        
        // eslint-disable-next-line new-cap
        const doc = new jsPDF();
        
        // Título
        doc.setFontSize(20);
        doc.setFont('helvetica', 'bold');
        doc.text('Relatório de Desacordos de Anotações', 14, 20);
        
        // Informações do projeto
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        const projectName = this.safeProject.name || 'Projeto sem nome';
        const threshold = this.safeProject.minPercentage || 80;
        const totalItems = this.filteredDiscrepancyItems.length;
        const discrepantItems = this.filteredDiscrepancyItems.filter(item => item.percentage < threshold).length;
        
        doc.text(`Projeto: ${projectName}`, 14, 35);
        doc.text(`Limiar de Concordância: ${threshold}%`, 14, 43);
        doc.text(`Total de Itens Analisados: ${totalItems}`, 14, 51);
        doc.text(`Itens com Desacordo: ${discrepantItems}`, 14, 59);
        doc.text(`Data do Relatório: ${new Date().toLocaleDateString('pt-PT')}`, 14, 67);
        
        // Linha separadora
        doc.setLineWidth(0.5);
        doc.line(14, 75, 196, 75);
        
        // Preparar dados da tabela - TODOS os itens, não apenas os discrepantes
        const tableData = this.filteredDiscrepancyItems.map(item => [
          // Documento (truncado)
          item.document && item.document.length > 40 
            ? item.document.substring(0, 40) + '...' 
            : item.document || 'N/A',
          // Label
          item.label || 'N/A',
          // Anotador
          item.annotator || 'N/A',
          // Taxa de concordância
          `${parseFloat(item.percentage || 0).toFixed(1)}%`,
          // Status
          item.status || 'N/A'
        ]);
        
        console.log('📋 Dados da tabela preparados:', tableData);
        
        // Criar tabela
        autoTable(doc, {
          startY: 85,
          head: [['Documento', 'Label', 'Anotador', 'Concordância', 'Status']],
          body: tableData,
          theme: 'striped',
          headStyles: {
            fillColor: [63, 81, 181],
            textColor: 255,
            fontSize: 10,
            fontStyle: 'bold'
          },
          bodyStyles: {
            fontSize: 9,
            cellPadding: 3
          },
          columnStyles: {
            0: { cellWidth: 50 }, // Documento
            1: { cellWidth: 30 }, // Label
            2: { cellWidth: 40 }, // Anotador
            3: { cellWidth: 25, halign: 'center' }, // Concordância
            4: { cellWidth: 35, halign: 'center' } // Status
          },
          margin: { left: 14, right: 14 },
          didParseCell(data) {
            // Colorir células de status
            if (data.column.index === 4) { // Coluna Status
              const cellValue = data.cell.text[0];
              if (cellValue && cellValue.includes('Divergentes')) {
                data.cell.styles.textColor = [244, 67, 54]; // Vermelho
                data.cell.styles.fontStyle = 'bold';
              } else if (cellValue && cellValue.includes('Consenso')) {
                data.cell.styles.textColor = [76, 175, 80]; // Verde
                data.cell.styles.fontStyle = 'bold';
              }
            }
            // Colorir células de concordância
            if (data.column.index === 3) { // Coluna Concordância
              const percentage = parseFloat(data.cell.text[0]);
              if (percentage < threshold) {
                data.cell.styles.fillColor = [255, 235, 238]; // Fundo vermelho claro
                data.cell.styles.textColor = [244, 67, 54]; // Texto vermelho
              } else {
                data.cell.styles.fillColor = [232, 245, 233]; // Fundo verde claro
                data.cell.styles.textColor = [76, 175, 80]; // Texto verde
              }
            }
          }
        });
        
        // Adicionar resumo no final
        const finalY = doc.lastAutoTable.finalY + 15;
        doc.setFontSize(10);
        doc.setFont('helvetica', 'italic');
        doc.text('Relatório gerado automaticamente pelo sistema Doccano', 14, finalY);
        doc.text(`Página 1 de 1 - ${new Date().toLocaleString('pt-PT')}`, 14, finalY + 8);
        
        // Salvar o PDF
        const pdfBlob = doc.output('blob');
        
        // Para browsers antigos como o IE
        if (window.navigator && window.navigator.msSaveOrOpenBlob) {
          window.navigator.msSaveOrOpenBlob(pdfBlob, `${filename}.pdf`);
          return;
        }
        
        // Para browsers modernos
        const url = URL.createObjectURL(pdfBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${filename}.pdf`;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        
        // Limpar recursos após download (sem redirecionamento)
        setTimeout(() => {
          URL.revokeObjectURL(url);
          document.body.removeChild(link);
          console.log('✅ PDF exportado com sucesso!');
        }, 100);
        
      } catch (error) {
        console.error('❌ Erro ao gerar PDF:', error);
        throw new Error(`Não foi possível gerar o PDF: ${error.message}`);
      }
    },
    getStatusIcon(item) {
      if (item.status === 'Consenso não alcançado') {
        return 'mdi-alert-circle';
      } else {
        return 'mdi-check-circle';
      }
    }
  }
}
</script>

<style scoped>
/* Dashboard Layout */
.disagreements-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.stats-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.action-buttons {
  position: relative;
  z-index: 2;
}

/* Main Content */
.main-content {
  margin-top: -30px;
  position: relative;
  z-index: 3;
}

/* Filter Card */
.filter-card {
  border-radius: 16px !important;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  border: 1px solid rgba(0,0,0,0.05);
}

.filter-card .v-card__title {
  background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px 16px 0 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.filter-select {
  transition: all 0.3s ease;
}

.filter-select:hover {
  transform: translateY(-2px);
}

.clear-filters-btn {
  transition: all 0.3s ease;
  font-weight: 600;
}

.clear-filters-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
}

/* Search Card */
.search-card {
  border-radius: 12px !important;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
}

.search-field {
  font-size: 16px;
}

/* Data Card */
.data-card {
  border-radius: 20px !important;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1) !important;
}

.data-card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px !important;
}

/* Table Styles */
.modern-table {
  background: transparent;
}

.modern-table >>> .v-data-table__wrapper {
  border-radius: 0;
}

.modern-table >>> .v-data-table-header {
  background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
}

.modern-table >>> .v-data-table-header th {
  font-weight: 600 !important;
  color: #495057 !important;
  border-bottom: 2px solid #dee2e6 !important;
  padding: 16px !important;
}

.modern-table >>> tbody tr {
  transition: all 0.2s ease;
}

.modern-table >>> tbody tr:hover {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.modern-table >>> tbody td {
  padding: 16px !important;
  border-bottom: 1px solid rgba(0,0,0,0.05) !important;
}

/* Cell Styles */
.document-cell {
  max-width: 250px;
}

.document-text {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 500;
  color: #495057;
  cursor: help;
}

.annotator-cell {
  display: flex;
  align-items: center;
  color: #6c757d;
}

.percentage-cell {
  min-width: 120px;
}

.details-btn {
  transition: all 0.3s ease;
}

.details-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Loading and Empty States */
.loading-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.empty-state {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
}

/* Details Dialog */
.details-dialog {
  border-radius: 16px !important;
  overflow: hidden;
}

.details-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px !important;
}

.details-list {
  background: transparent;
}

.details-item {
  border-radius: 12px;
  margin-bottom: 8px;
  transition: all 0.2s ease;
  background: rgba(0,0,0,0.02);
}

.details-item:hover {
  background: rgba(102, 126, 234, 0.05);
  transform: translateX(4px);
}

.details-item >>> .v-list-item__avatar {
  margin-right: 16px;
}

/* Responsive Design */
@media (max-width: 960px) {
  .hero-section .display-1 {
    font-size: 2rem !important;
  }
  
  .stats-chips {
    justify-content: center;
  }
  
  .action-buttons {
    margin-top: 24px;
  }
  
  .main-content {
    margin-top: -20px;
  }
}

@media (max-width: 600px) {
  .hero-section {
    padding: 32px 0;
  }
  
  .hero-section .display-1 {
    font-size: 1.75rem !important;
  }
  
  .filter-card,
  .search-card,
  .data-card {
    margin: 0 8px;
  }
  
  .document-cell {
    max-width: 150px;
  }
  
  .modern-table >>> tbody td {
    padding: 12px 8px !important;
  }
}

/* Animation Classes */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active {
  transition: all 0.3s ease;
}

.slide-up-enter {
  transform: translateY(30px);
  opacity: 0;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}
</style> 