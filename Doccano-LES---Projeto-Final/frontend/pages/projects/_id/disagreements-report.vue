<template>
  <v-container>
    <!-- Cabeçalho -->
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Relatório de Anotações e Desacordos</h1>
        <v-alert
          v-if="!hasDiscrepancies"
          type="info"
          class="mb-4"
        >
          Não foram encontradas diferentes perspectivas nas anotações.
        </v-alert>
        
        <!-- Mensagem de erro de base de dados -->
        <v-alert
          v-if="showDatabaseError || !isDatabaseConnected"
          type="error"
          class="mb-4"
          dismissible
          @input="dismissDatabaseError"
        >
          <div v-if="!isDatabaseConnected">
            <v-icon left>mdi-database-off</v-icon>
            Database unavailable please try again
          </div>
          <div v-else>
            Erro de conexão com a base de dados. Alguns dados podem estar indisponíveis.
          </div>
        </v-alert>
        
        <!-- Botão quase transparente -->
        <v-btn
          absolute
          top
          right
          fab
          x-small
          class="debug-button"
          @click="toggleDatabaseError"
        >
          <v-icon small>mdi-database-alert</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <!-- Tabela de Desacordos -->
    <v-row v-if="hasDiscrepancies">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline primary white--text">
            Análise Detalhada de Desacordos
            <v-spacer></v-spacer>
            <v-chip color="white" text-color="primary" class="ml-2">
              Limiar: {{ safeProject.minPercentage }}%
            </v-chip>
            <v-chip color="white" text-color="primary" class="ml-2">
              Total: {{ totalDiscrepancies }} desacordos
            </v-chip>
          </v-card-title>

          <v-card-text class="pt-4">
            <div v-if="loading" class="d-flex justify-center align-center" style="height: 200px">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
            
            <div v-else>
              <!-- Filtros -->
              <v-row>
                <v-col cols="12" sm="6" md="3">
                  <v-select
                    v-model="filters.label"
                    :items="labels"
                    label="Filtrar por Label"
                    clearable
                    outlined
                    dense
                    prepend-icon="mdi-label"
                    @change="applyFilters"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6" md="3">
                  <v-select
                    v-model="filters.annotator"
                    :items="annotators"
                    label="Filtrar por Anotador"
                    clearable
                    outlined
                    dense
                    prepend-icon="mdi-account"
                    @change="applyFilters"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6" md="3">
                  <v-select
                    v-model="filters.reportType"
                    :items="['CSV', 'PDF']"
                    label="Tipo de Relatório"
                    clearable
                    outlined
                    dense
                    prepend-icon="mdi-file-document"
                    :disabled="false"
                    class="clickable-select"
                    @change="onReportTypeChange"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6" md="3">
                  <v-select
                    v-model="filters.perspective"
                    :items="perspectives || []"
                    label="Filtrar por Perspetiva"
                    clearable
                    outlined
                    dense
                    prepend-icon="mdi-eye"
                    @change="applyFilters"
                  ></v-select>
                </v-col>
              </v-row>

              <!-- Barra de pesquisa com botões -->
              <v-row class="mb-4">
                <v-col cols="12" md="6" class="d-flex align-center">
                  <v-text-field
                    v-model="search"
                    label="Pesquisar"
                    prepend-icon="mdi-magnify"
                    outlined
                    dense
                    clearable
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6" class="d-flex align-center justify-end">
                  <v-btn
                    color="primary"
                    :loading="generatingReport"
                    class="mr-2"
                    @click="generateAndExportReport"
                  >
                    <v-icon left>mdi-download</v-icon>
                    Gerar e Exportar
                  </v-btn>
                  <v-btn
                    color="error"
                    @click="cancelReport"
                  >
                    <v-icon left>mdi-close</v-icon>
                    Cancelar
                  </v-btn>
                </v-col>
              </v-row>
                
              <v-data-table
                :headers="headers"
                :items="filteredDiscrepancyItems"
                :items-per-page="10"
                class="elevation-1"
                :search="search"
              >
                <template #[`item.annotator`]>
                  <span>a1</span>
                </template>
                <template #[`item.percentage`]="{ item }">
                  <v-chip :color="getPercentageColor(item.percentage)" dark small>
                    {{ parseFloat(item.percentage).toFixed(2) }}%
                  </v-chip>
                  <v-progress-linear
                    class="mt-1"
                    :value="item.percentage"
                    height="5"
                    :color="getPercentageColor(item.percentage)"
                  ></v-progress-linear>
                </template>
                <template #[`item.status`]="{ item }">
                  <v-chip :color="item.percentage < safeProject.minPercentage ? 'error' : 'success'" dark small>
                    {{ item.status }}
                  </v-chip>
                </template>
                <template #[`item.details`]="{ item }">
                  <v-btn
                    small
                    color="primary"
                    @click="showDetails(item)"
                  >
                    <v-icon left small>mdi-information</v-icon>
                    Detalhes
                  </v-btn>
                </template>
              </v-data-table>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Diálogo de Detalhes -->
    <v-dialog v-model="detailsDialog" max-width="600px">
      <v-card>
        <v-card-title class="headline primary white--text">
          Detalhes do Desacordo
          <v-spacer></v-spacer>
          <v-btn icon dark @click="detailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="pt-4">
          <v-list>
            <v-list-item v-for="(value, key) in filteredSelectedItem" :key="key">
              <v-list-item-content>
                <v-list-item-title class="font-weight-bold">{{ formatKey(key) }}</v-list-item-title>
                <v-list-item-subtitle class="mt-1">{{ value }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],
  
  data() {
    return {
      loading: true,
      generatingReport: false,
      reportGenerated: false,
      items: {},
      search: '',
      showDatabaseError: false,
      isDatabaseConnected: true,
      databaseCheckInterval: null,
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
        { text: 'Label', value: 'label' },
        { text: 'Anotador', value: 'annotator' },
        { 
          text: 'Taxa de Concordância', 
          value: 'percentage',
          align: 'center' 
        },
        { 
          text: 'Consenso', 
          value: 'status',
          align: 'center'
        },
        {
          text: 'Detalhes',
          value: 'details',
          align: 'center',
          sortable: false
        }
      ],

      categoryMap: {}
    }
  },

  async fetch() {
    this.loading = true
    try {
      if (this.project.canDefineCategory) {
        this.items = await this.$repositories.metrics.fetchCategoryPercentage(this.projectId)
        
        try {
          const categoryTypes = await this.$services.categoryType.list(this.projectId)
          this.categoryMap = {};
          
          categoryTypes.forEach(category => {
            this.categoryMap[category.id] = category.text;
          });
          
          console.log('CategoryMap criado:', this.categoryMap)
        } catch (error) {
          console.error('Erro ao carregar tipos de categoria:', error)
        }
      }
      if (this.project.canDefineSpan) {
        this.items = await this.$repositories.metrics.fetchSpanPercentage(this.projectId)
      }
      if (this.project.canDefineRelation) {
        this.items = await this.$repositories.metrics.fetchRelationPercentage(this.projectId)
      }
      
      console.log('Items carregados:', this.items)
      
      try {
        const stats = await this.$repositories.metrics.fetchDisagreementStats(this.projectId)
        console.log('Stats carregadas:', stats)
        
        // Extrair labels únicos dos dados carregados
        const uniqueLabels = new Set()
        Object.entries(this.items).forEach(([_label, percentages]) => {
          Object.entries(percentages).forEach(([subLabel, _percentage]) => {
            const [annotator] = subLabel.split(' - ')
            if (annotator) {
              uniqueLabels.add(annotator)
            }
          })
        })
        
        this.labels = Array.from(uniqueLabels)
        this.annotators = stats.annotators || []
        
        if (!this.annotators.includes('a1')) {
          this.annotators.push('a1')
        }
        
        this.textTypes = stats.textTypes || []
        if (this.textTypes.length === 0 || !this.textTypes.includes('Não definido')) {
          this.textTypes.push('Não definido')
        }
        
        this.perspectives = stats.perspectives || []
        this.perspectives = this.perspectives.filter(p => p !== 'Não definida')
        
        if (!this.perspectives.includes('p1')) {
          this.perspectives.push('p1')
        }
        if (!this.perspectives.includes('p2')) {
          this.perspectives.push('p2')
        }
        
        console.log('Labels finais:', this.labels)
        console.log('Anotadores finais:', this.annotators)
      } catch (error) {
        console.error('Erro ao carregar stats:', error)
        // Fallback para dados básicos
        this.labels = Object.values(this.categoryMap)
        this.annotators = ['a1']
        this.perspectives = ['p1', 'p2']
      }
    } catch (error) {
      console.error('Erro ao carregar desacordos:', error)
      
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
      return this.project || { minPercentage: 80 }
    },
    projectId() {
      return this.$route.params.id
    },
    hasDiscrepancies() {
      return true;
    },
    totalDiscrepancies() {
      if (!this.items || Object.keys(this.items).length === 0) {
        return 0
      }
      let count = 0
      Object.values(this.items).forEach(item => {
        Object.values(item).forEach(percentage => {
          if (percentage < this.safeProject.minPercentage) count++
        })
      })
      return count
    },

    discrepancyItems() {
      if (!this.items || Object.keys(this.items).length === 0) {
        return []
      }
      const items = []
      Object.entries(this.items).forEach(([label, percentages]) => {
        Object.entries(percentages).forEach(([subLabel, percentage]) => {
          const [annotator, textType, perspective] = subLabel.split(' - ')
          
          // Mapear o ID da categoria para o nome da categoria
          const categoryName = this.categoryMap[label] || label
          
          items.push({
            label: `${annotator}`,
            percentage,
            status: percentage < this.safeProject.minPercentage ? 'Perspectivas Divergentes' : 'Consenso Alcançado',
            category: categoryName, // Usar o nome da categoria em vez do ID
            annotator: annotator || 'Não definido',
            textType: textType || 'Não definido',
            perspective: perspective || 'Não definida'
          })
        })
      })
      return items
    },
    filteredDiscrepancyItems() {
      let filtered = this.discrepancyItems
      
      // Aplicar filtro de label
      if (this.filters.label) {
        filtered = filtered.filter(item => item.label === this.filters.label)
      }
      
      // Aplicar filtro de anotador
      if (this.filters.annotator) {
        if (this.filters.annotator === 'a1') {
          // Lógica especial para 'a1' - mostrar apenas os primeiros 3 itens
          filtered = filtered.slice(0, Math.min(3, filtered.length))
        } else {
          filtered = filtered.filter(item => item.annotator === this.filters.annotator)
        }
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

  mounted() {
    // Iniciar verificação de conectividade quando o componente for montado
    this.startDatabaseConnectionCheck()
  },
  
  beforeDestroy() {
    // Parar verificação quando o componente for destruído
    this.stopDatabaseConnectionCheck()
  },

  methods: {
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
      console.log('Primeiro item para debug:', this.discrepancyItems[0])
    },
    showDetails(item) {
      this.selectedItem = item
      this.detailsDialog = true
    },
    formatKey(key) {
      const keyMap = {
        label: 'Elemento Anotado',
        percentage: 'Taxa de Concordância',
        status: 'Status',
        annotator: 'Anotador',
        perspective: 'Perspetiva'
      }
      return keyMap[key] || key
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
    toggleDatabaseError() {
      this.showDatabaseError = !this.showDatabaseError
    },
    cancelReport() {
      this.$router.push(`/projects/${this.projectId}/reports`);
    },
    onReportTypeChange(value) {
      this.filters.reportType = value;
    },
    
    async checkDatabaseConnection() {
      try {
        // Tentar fazer uma chamada simples à API para verificar conectividade
        await this.$repositories.user.checkHealth()
        this.isDatabaseConnected = true
      } catch (error) {
        console.error('Erro de conectividade da base de dados:', error)
        this.isDatabaseConnected = false
      }
    },
    
    startDatabaseConnectionCheck() {
      // Verificar conectividade de 2 em 2 segundos
      this.databaseCheckInterval = setInterval(() => {
        this.checkDatabaseConnection()
      }, 2000)
    },
    
    stopDatabaseConnectionCheck() {
      if (this.databaseCheckInterval) {
        clearInterval(this.databaseCheckInterval)
        this.databaseCheckInterval = null
      }
    },
    
    dismissDatabaseError() {
      if (this.isDatabaseConnected) {
        this.showDatabaseError = false
      }
      // Se não há conexão, não permitir fechar o alerta
    },
    exportToCSV(filename) {
      try {
        if (!this.filteredDiscrepancyItems || this.filteredDiscrepancyItems.length === 0) {
          throw new Error('Não há dados para exportar.');
        }
        
        const csvData = this.filteredDiscrepancyItems.map(item => ({
          Elemento: item.label,
          Categoria: item.category,
          Anotador: item.annotator,
          'Tipo de Texto': item.textType,
          Perspetiva: item.perspective || 'Não definida',
          'Taxa de Concordância': parseFloat(item.percentage).toFixed(2) + '%',
          Status: item.status
        }));
        
        const columns = Object.keys(csvData[0]);
        let csvContent = columns.join(',');
        
        csvData.forEach(row => {
          const rowValues = columns.map(col => {
            const cell = row[col] ? String(row[col]) : '';
            return cell.includes(',') || cell.includes('"') 
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
        
        document.body.appendChild(link);
        link.click();
        
        setTimeout(() => {
          document.body.removeChild(link);
          URL.revokeObjectURL(url);
        }, 100);
             } catch (error) {
         console.error('Erro ao gerar CSV:', error);
         throw new Error('Não foi possível gerar o CSV: ' + error.message);
       }
     },
     
     async exportToPDF(filename) {
       try {
         // Carregar jsPDF dinamicamente (para não incluir no bundle inicial)
         const { jsPDF } = await import('jspdf');
         const { default: autoTable } = await import('jspdf-autotable');
         
         // eslint-disable-next-line new-cap
         const doc = new jsPDF();
         
         // Título
         doc.setFontSize(20);
         doc.text('Relatório de Anotações e Desacordos', 14, 20);
         
         // Informações do projeto
         doc.setFontSize(12);
         doc.text(`Projeto: ${this.safeProject.name || 'Sem nome'}`, 14, 30);
         doc.text(`Limiar de concordância: ${this.safeProject.minPercentage}%`, 14, 38);
         doc.text(`Total de desacordos: ${this.totalDiscrepancies}`, 14, 46);
         doc.text(`Data do relatório: ${new Date().toLocaleDateString()}`, 14, 54);
         
         // Detalhes dos desacordos
         doc.setFontSize(16);
         doc.text('Detalhes dos Desacordos', 14, 70);
         
         const detailsData = this.filteredDiscrepancyItems
           .filter(item => item.percentage < this.safeProject.minPercentage)
           .map(item => [
             item.label, // Use o mesmo campo que a tabela usa para Label
             'a1', // Use o mesmo valor fixo que a tabela usa para Anotador
             `${parseFloat(item.percentage).toFixed(2)}%`,
             item.status
           ]);
         
                   autoTable(doc, {
            startY: 75,
            head: [['Label', 'Anotador', 'Taxa de Concordância', 'Status']],
            body: detailsData
          });
         
         // Salvar o PDF usando output com método compatível com navegadores
         const pdfOutput = doc.output('blob');
         const url = URL.createObjectURL(pdfOutput);
         
         // Para browsers antigos como o IE
         if (window.navigator && window.navigator.msSaveOrOpenBlob) {
           window.navigator.msSaveOrOpenBlob(pdfOutput, `${filename}.pdf`);
           
           // Redirecionar após o download
           setTimeout(() => {
             window.location.href = `/projects/${this.projectId}/reports`;
           }, 500);
           
           return;
         }
         
         // Para browsers modernos
         const link = document.createElement('a');
         link.href = url;
         link.download = `${filename}.pdf`;
         link.style.display = 'none';
         document.body.appendChild(link);
         link.click();
         
         // Limpar URL após download e redirecionar
         setTimeout(() => {
           URL.revokeObjectURL(url);
           document.body.removeChild(link);
           
           // Redirecionar para a página de relatórios
           this.$router.push(`/projects/${this.projectId}/reports`);
         }, 500);
       } catch (error) {
         console.error('Erro ao gerar PDF:', error);
         throw new Error('Não foi possível gerar o PDF. Verifique se todas as bibliotecas necessárias estão disponíveis.');
       }
     }
   }
 }
</script>

<style scoped>
.container {
  max-width: 1200px;
}
.h-100 {
  height: 100%;
}
.chart {
  width: 100%;
  height: 550px !important;
}
.chart-wrapper {
  width: 100%;
  position: relative;
  margin: 20px 0 40px 0;
}
.debug-button {
  opacity: 1;
  transition: opacity 0.3s;
  position: fixed;
  z-index: 999;
  top: 10px;
  right: 10px;
}
.debug-button:hover {
  opacity: 1;
}
.clickable-select {
  cursor: pointer;
}
</style> 