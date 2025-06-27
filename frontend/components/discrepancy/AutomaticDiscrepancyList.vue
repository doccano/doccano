<template>
  <div class="container">
    

    <v-data-table
      :items="processedItems"
      :headers="headers"
      :loading="isLoading"
      loading-text="Carregando..."
      no-data-text="Nenhum dado disponível"
      :footer-props="{
        showFirstLastPage: true,
        'items-per-page-options': [10, 50, 100],
        'items-per-page-text': 'Itens por página:',
        'page-text': '{0}-{1} de {2}'
      }"
      item-key="id"
      @input="$emit('input', $event)"
    >
      <template #top>
        <v-row class="mb-3">
          <v-col cols="12" md="6">
            <v-text-field
              v-model="search"
              :prepend-inner-icon="mdiMagnify"
              label="Search"
              single-line
              hide-details
              filled
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedAnnotationFilter"
              :items="annotationFilterOptions"
              label="Filter by Text"
              prepend-inner-icon="mdi-filter"
              clearable
              hide-details
              filled
            />
          </v-col>
        </v-row>
      </template>

      <template #[`item.text`]="{ item }">
        <span class="d-flex d-sm-none">{{ item.text.length > 50 ? item.text.substring(0, 50) + '...' : item.text }}</span>
        <span class="d-none d-sm-flex">{{ item.text.length > 200 ? item.text.substring(0, 200) + '...' : item.text }}</span>
      </template>


      <template #[`item.annotations`]="{ item }">
        <div style="white-space: pre-line;">{{ item.annotationsText }}</div>
      </template>

      <template #[`item.labelPercentages`]="{ item }">
        <div v-if="item.labelPercentages && Object.keys(item.labelPercentages).length > 0">
          <div v-for="(percentage, label) in item.labelPercentages" :key="label" class="automatic-label-percentage">
            <v-badge
              :content="percentage + '%'"
              :color="getAutomaticLabelColor(String(label))"
              overlap
              class="mr-2 mb-1"
            >
              <v-chip 
                small 
                :color="getAutomaticLabelColor(String(label))" 
                outlined
                class="font-weight-bold"
                style="border-width: 2px;"
              >
                {{ label }}
              </v-chip>
            </v-badge>
          </div>
        </div>
        <span v-else class="text--disabled font-italic">No data available</span>
      </template>

      <template #[`item.alignment`]="{ item }">
        <div class="alignment-info">
          <v-progress-linear
            :value="item.alignmentPercentage"
            height="12"
            :color="getAlignmentColor(item.alignmentPercentage)"
            class="mb-1"
            rounded
          ></v-progress-linear>
          <span class="percentage-text font-weight-medium">{{ item.alignmentPercentage }}%</span>
        </div>
      </template>

<template #[`item.status`]="{ item }">
  <v-chip v-if="item.hasDiscrepancy" color="error" small>
    Discrepant
  </v-chip>
  <v-chip v-else color="success" small>
    Non Discrepant
  </v-chip>
</template>



    </v-data-table>
  </div>
</template>


<script lang="ts">
import Vue from 'vue'
import { mdiMagnify, mdiAlertCircle } from '@mdi/js'
import type { PropType } from 'vue'

type ExampleDTO = {
  id: number
  text: string
  annotations: Array<{
    user: number
    label: string
    start_offset: number
    end_offset: number
  }>
}


export default Vue.extend({
  name: 'AutomaticDiscrepancyList',
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<ExampleDTO[]>,
      default: () => [],
      required: true
    },
    members: {
      type: Array as PropType<any[]>,
      default: () => [],
      required: true
    },
    databaseError: {
      type: Boolean,
      default: false,
      required: false
    }
  },

  data() {
    return {
      search: '',
      mdiMagnify,
      mdiAlertCircle,
      memberNames: {} as { [key: number]: string },
      selectedAnnotationFilter: null as string | null
    }
  },

  computed: {
    headers() {
      return [
        { text: 'Text', value: 'text', sortable: true },
        { text: 'Label Percentage', value: 'labelPercentages', sortable: false },
        { text: 'Alignment', value: 'alignment', sortable: false },
        { text: 'Status', value: 'status', sortable: false }
      ]
    },
    projectId(): string {
      return this.$route.params.id
    },

    annotationFilterOptions() {
      const annotatedTexts = new Set<string>()
      
      this.items.forEach(item => {
        if (item.annotations && Array.isArray(item.annotations) && item.annotations.length > 0) {
          annotatedTexts.add(item.text) // Valor completo para filtro
        }
      })
      
      return Array.from(annotatedTexts).sort().map(text => ({
        text: text.length > 80 ? text.substring(0, 80) + '...' : text, // Texto truncado para exibição
        value: text // Texto completo para filtro
      }))
    },
    processedItems() {
  console.log('📦 Anotações recebidas:', JSON.stringify(this.items, null, 2))

  const result: Array<{
    id: number
    text: string
    annotationsText: string
    hasDiscrepancy: boolean
    discrepancyDetails: string
    labelPercentages: { [label: string]: number }
    alignmentPercentage: number
  }> = []

  // Agrupar anotações por documento (não por usuário e documento)
  const processedDocIds = new Set<number>()
  const annotationsByDoc: { [docId: number]: { [memberId: number]: any[] } } = {}

  // Primeiro passo: agrupar todas as anotações por documento
  this.items.forEach(item => {
    if (item.annotations && Array.isArray(item.annotations)) {
      if (!annotationsByDoc[item.id]) {
        annotationsByDoc[item.id] = {}
      }
      item.annotations.forEach((annotation: any) => {
        const userId = annotation.user ?? annotation.user_id ?? annotation.created_by
        if (userId) {
          if (!annotationsByDoc[item.id][userId]) {
            annotationsByDoc[item.id][userId] = []
          }
          annotationsByDoc[item.id][userId].push(annotation)
        }
      })
    }
  })

  // Segundo passo: processar cada documento apenas uma vez
  Object.keys(annotationsByDoc).forEach(docIdStr => {
    const docId = parseInt(docIdStr)
    if (processedDocIds.has(docId)) return
    processedDocIds.add(docId)
    
    const annotations = annotationsByDoc[docId]
    if (!annotations) return

    const memberIds = Object.keys(annotations).map(id => parseInt(id))
    if (memberIds.length <= 1) return

    // Encontrar o documento correspondente
    const item = this.items.find(i => i.id === docId)
    if (!item) return

    let discrepancyDetails = ''
    let annotationsText = ''

    for (let i = 0; i < memberIds.length; i++) {
      const memberId = memberIds[i]
      const memberAnnotations = annotations[memberId]
      const memberName = this.memberNames[memberId] || `Usuário ${memberId}`
      annotationsText += `${memberName}: ${this.formatAnnotations(memberAnnotations)}\n`

      for (let j = i + 1; j < memberIds.length; j++) {
        const otherMemberId = memberIds[j]
        const otherAnnotations = annotations[otherMemberId]
        const discrepancy = this.compareAnnotations(memberAnnotations, otherAnnotations)
        if (discrepancy) {
          const otherMemberName = this.memberNames[otherMemberId] || `Usuário ${otherMemberId}`
          discrepancyDetails += `Discrepancy between ${memberName} and ${otherMemberName}:\n${discrepancy}\n\n`
        }
      }
    }

    if (this.search) {
      const searchLower = this.search.toLowerCase()
      if (!item.text.toLowerCase().includes(searchLower) &&
          !annotationsText.toLowerCase().includes(searchLower)) return
    }

    // Filtrar por texto selecionado
    if (this.selectedAnnotationFilter) {
      if (item.text !== this.selectedAnnotationFilter) return
    }

    // Calcular porcentagens de labels
    const labelCounts: { [label: string]: number } = {}
    const totalAnnotations: { [label: string]: number } = {}
    
    // Contar ocorrências de cada label
    Object.values(annotations).forEach(memberAnnotations => {
      memberAnnotations.forEach((annotation: any) => {
        if (annotation.label) {
          if (!labelCounts[annotation.label]) {
            labelCounts[annotation.label] = 0
            totalAnnotations[annotation.label] = 0
          }
          labelCounts[annotation.label]++
          totalAnnotations[annotation.label]++
        }
      })
    })
    
    // Calcular porcentagens
    const labelPercentages: { [label: string]: number } = {}
    const totalLabels = Object.values(totalAnnotations).reduce((sum, count) => sum + count, 0)
    
    if (totalLabels > 0) {
      Object.keys(labelCounts).forEach(label => {
        labelPercentages[label] = Math.round((labelCounts[label] / totalLabels) * 100)
      })
    }
    
    // Calcular alignment baseado no threshold do projeto
    const threshold = this.$store.getters['projects/project'].labelDiscrepancyThreshold || 0
    
    // Calcular percentagem da label mais comum
    let alignmentPercentage = 0
    
    if (memberIds.length > 0) {
      // Contar todas as labels de todos os anotadores
      const labelCounts: { [label: string]: number } = {}
      let totalLabels = 0
      
      memberIds.forEach(memberId => {
        const memberAnnotations = annotations[memberId]
        if (memberAnnotations && memberAnnotations.length > 0) {
          memberAnnotations.forEach((annotation: any) => {
            if (annotation.label) {
              labelCounts[annotation.label] = (labelCounts[annotation.label] || 0) + 1
              totalLabels++
            }
          })
        }
      })
      
      if (totalLabels > 0) {
        // Encontrar a label mais frequente
        let maxCount = 0
        Object.values(labelCounts).forEach(count => {
          if (count > maxCount) {
            maxCount = count
          }
        })
        
        // Calcular percentagem da label mais comum
        alignmentPercentage = Math.round((maxCount / totalLabels) * 100)
      }
    }
    
    // Determinar se é discrepant baseado no threshold
    const isDiscrepant = alignmentPercentage < threshold
    
    result.push({
      id: docId,
      text: item.text,
      annotationsText,
      hasDiscrepancy: isDiscrepant,
      discrepancyDetails,
      labelPercentages,
      alignmentPercentage
    })
  })

  return result
}

  },

  watch: {
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
  this.loadMemberNames()
  this.loadLabelsIfNeeded()
},


  methods: {
    formatAnnotations(annotations: any[]): string {
      if (!annotations || annotations.length === 0) return 'Sem anotações'
      return annotations.map(a => {
        if (a.label !== undefined) return `Label: ${a.label}`
        if (a.text !== undefined) return a.text
        return JSON.stringify(a)
      }).join(', ')
    },

loadLabelsIfNeeded() {
  const labels = this.$store.getters['labels/list']
  if (!labels || labels.length === 0) {
    this.$store.dispatch('labels/fetch', this.projectId).catch(error => {
      console.warn('Erro ao carregar labels:', error)
    })
  }
},


    getLabelName(labelId: string): string {
  // Se você tiver um mapeamento global com os nomes das labels (ex: this.$store.getters['labels/list'])
  const label = this.$store.getters['labels/list']?.find((l: any) => l.id.toString() === labelId)
  return label ? label.text : labelId
},
    
    getLabelColor(label: string): string {
      // Gerar uma cor consistente baseada no nome do label
      const colors = ['primary', 'secondary', 'success', 'info', 'warning', 'error', 'purple', 'indigo', 'cyan', 'teal', 'orange']
      const hash = label.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      return colors[hash % colors.length]
    },

    getAutomaticLabelColor(label: string): string {
      // Paleta de cores primárias e fortes para automatic discrepancies
      const automaticColors = ['blue darken-3', 'green darken-3', 'red darken-1', 'orange darken-2', 'purple darken-2', 'teal darken-2', 'indigo darken-2', 'brown darken-2', 'blue-grey darken-3', 'deep-orange darken-1']
      const hash = label.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      return automaticColors[hash % automaticColors.length]
    },
    
    getParticipationColor(rate: number): string {
      if (rate < 30) return 'error'
      if (rate < 60) return 'warning'
      return 'success'
    },

    getAlignmentColor(alignmentPercentage: number): string {
      const threshold = this.$store.getters['projects/project'].labelDiscrepancyThreshold || 0
      if (alignmentPercentage >= threshold) return 'success'
      if (alignmentPercentage >= threshold * 0.7) return 'warning'
      return 'error'
    },

    truncate(value: string, length: number): string {
  if (!value || typeof value !== 'string') return ''
  return value.length > length ? value.slice(0, length) + '...' : value
},


    compareAnnotations(annotations1: any[], annotations2: any[]): string | null {
      const differences: string[] = []


      const spans1 = annotations1.filter(a => a.start_offset !== undefined).sort((a, b) => a.start_offset - b.start_offset)
      const spans2 = annotations2.filter(a => a.start_offset !== undefined).sort((a, b) => a.start_offset - b.start_offset)

      if (spans1.length !== spans2.length) {
        differences.push(`Número diferente de spans: ${spans1.length} vs ${spans2.length}`)
      } else {
        for (let i = 0; i < spans1.length; i++) {
          if (spans1[i].label !== spans2[i].label ||
              spans1[i].start_offset !== spans2[i].start_offset ||
              spans1[i].end_offset !== spans2[i].end_offset) {
            differences.push(`Span diferente: "${spans1[i].start_offset}-${spans1[i].end_offset}:${spans1[i].label}" vs "${spans2[i].start_offset}-${spans2[i].end_offset}:${spans2[i].label}"`)
          }
        }
      }

      const categories1 = annotations1.filter(a => a.label !== undefined && a.start_offset === undefined)
      const categories2 = annotations2.filter(a => a.label !== undefined && a.start_offset === undefined)

      if (categories1.length !== categories2.length) {
        differences.push(`Número diferente de categorias: ${categories1.length} vs ${categories2.length}`)
      } else {
        const labels1 = new Set<string>(categories1.map(c => c.label))
        const labels2 = new Set<string>(categories2.map(c => c.label))

        if (labels1.size !== labels2.size) {
          differences.push(`Número diferente de labels: ${labels1.size} vs ${labels2.size}`)
        } else {
          for (const label of labels1) {
            if (!labels2.has(label)) {
              differences.push(`Label diferente: "${label}" não encontrado no segundo conjunto`)
            }
          }
        }
      }

      return differences.length > 0 ? differences.join('\n') : null
    },

    loadMemberNames() {
      // Usar os dados dos members que já foram buscados na página principal
      this.members.forEach((member: any) => {
        this.$set(this.memberNames, member.id, member.username)
      })

      // Para qualquer member ID que não esteja na lista, usar um fallback
      const memberIds = new Set<number>()
      this.items.forEach(item => {
        if (item.annotations && Array.isArray(item.annotations)) {
          item.annotations.forEach((annotation: any) => {
            if (annotation.user && !this.memberNames[annotation.user]) {
              memberIds.add(annotation.user)
            }
          })
        }
      })

      // Só buscar members que não estão na lista já carregada
      memberIds.forEach(memberId => {
        this.$set(this.memberNames, memberId, `Usuário ${memberId}`)
      })
    },


  }
})
</script>

<style scoped>
.container {
  padding-left: 20px;
  padding-right: 20px;
  margin-top: 10px;
}

.pulse-animation {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 193, 7, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 193, 7, 0);
  }
}

.discrepancy-tooltip {
  max-width: 300px;
  white-space: pre-line;
  font-size: 14px;
}

.label-percentage {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.label-percentage .v-chip {
  font-size: 11px;
  padding: 0 8px;
  height: 24px;
  max-width: 120px;
  white-space: nowrap;
}

.label-percentage .v-progress-linear {
  width: 120px;
  height: 10px;
  border-radius: 4px;
  background-color: #f0f0f0;
  margin: 0;
}

.percentage-text {
  font-size: 12px;
  min-width: 32px;
  text-align: right;
}


.alignment-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 120px;
}

.automatic-label-percentage {
  display: inline-block;
  margin-right: 8px;
  margin-bottom: 8px;
}

.automatic-label-percentage .v-badge {
  position: relative;
}

.automatic-label-percentage .v-chip {
  transition: all 0.3s ease;
}

.automatic-label-percentage .v-chip:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
</style>
