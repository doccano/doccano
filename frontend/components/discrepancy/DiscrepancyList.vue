<template>
  <div class="container">
    <v-alert type="info" outlined dense class="mb-4">
      <strong>Attention!</strong> Discrepancies between annotations are highlighted with a pulsing yellow icon
      <v-chip color="warning" x-small class="mx-1"><v-icon x-small>{{ mdiAlertCircle }}</v-icon></v-chip> 
      in the Status column. 
    </v-alert>

    <v-checkbox
      v-model="showOnlyDiscrepancies"
      label="Show only discrepancies between annotations"
      class="mb-4"
    />

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
      :item-class="getRowClass"
      @input="$emit('input', $event)"
    >
      <template #top>
        <v-text-field
          v-model="search"
          :prepend-inner-icon="mdiMagnify"
          label="Search"
          single-line
          hide-details
          filled
        />
      </template>

      <template #[`item.text`]="{ item }">
        <span class="d-flex d-sm-none">{{ truncate(item.text, 50) }}</span>
        <span class="d-none d-sm-flex">{{ truncate(item.text, 200) }}</span>
      </template>


      <template #[`item.annotations`]="{ item }">
        <div style="white-space: pre-line;">{{ item.annotationsText }}</div>
      </template>

      <template #[`item.labelPercentages`]="{ item }">
        <div v-if="item.labelPercentages && Object.keys(item.labelPercentages).length > 0">
          <!-- Mostrar apenas as primeiras 2 labels -->
          <div
            v-for="label in Object.keys(item.labelPercentages).slice(0, 2)"
            :key="label"
            class="label-percentage"
          >
            <v-chip x-small :color="getLabelColor(label.toString())" class="mr-1 white--text">
              {{ getLabelName(label.toString()) }}
            </v-chip>
            <v-progress-linear
              :value="item.labelPercentages[label]"
              height="10"
              :color="getLabelColor(label.toString())"
              class="mb-1"
            ></v-progress-linear>
            <span class="percentage-text">{{ item.labelPercentages[label] }}%</span>
          </div>

          <!-- Botão "See More" sempre presente -->
          <v-btn
            x-small
            text
            color="primary"
            class="mt-1"
            @click="openLabelDialog(item)"
          >
            <span v-if="Object.keys(item.labelPercentages).length > 2">
              See More ({{ Object.keys(item.labelPercentages).length - 2 }}+)
            </span>
            <span v-else>
              See More
            </span>
          </v-btn>
        </div>
        <span v-else>No data</span>
      </template>

      <template #[`item.participation`]="{ item }">
        <div class="participation-info">
          <v-chip small :color="getParticipationColor(item.participationRate)">
            {{ item.participationCount }} de {{ item.totalMembers }}
          </v-chip>
          <v-progress-linear
            :value="item.participationRate"
            height="10"
            :color="getParticipationColor(item.participationRate)"
            class="mt-1"
          ></v-progress-linear>
          <span class="percentage-text">{{ item.participationRate }}%</span>
        </div>
      </template>

      <template #[`item.discrepancyPercentage`]="{ item }">
        <div class="discrepancy-info">
          <div class="d-flex align-center mb-2">
            <v-progress-circular
              :value="item.discrepancyData.disagreement"
              :color="getDiscrepancyColor(item.discrepancyPercentage)"
              size="40"
              width="4"
              class="mr-2"
            >
              <span class="caption">{{ item.discrepancyPercentage }}%</span>
            </v-progress-circular>
            <div>
              <div class="caption">
                <v-icon small color="success">mdi-check</v-icon>
                {{ item.discrepancyData.agreement }}% acordo
              </div>
              <div class="caption">
                <v-icon small :color="getDiscrepancyColor(item.discrepancyPercentage)">mdi-alert</v-icon>
                {{ item.discrepancyData.disagreement }}% discrepância
              </div>
            </div>
          </div>
        </div>
      </template>

<template #[`item.status`]="{ item }">
  <v-chip v-if="item.hasDiscrepancy" color="warning" small class="pulse-animation">
    <v-icon small left>{{ mdiAlertCircle }}</v-icon>
    Discrepancy
  </v-chip>
  <v-chip v-else color="success" small>
    Consistent
  </v-chip>
</template>


      <template #[`item.action`]="{ item }">
        <v-btn small color="primary text-capitalize" @click="viewAnnotation(item)">
          Annotate
        </v-btn>
      </template>
    </v-data-table>

    <!-- Dialog para mostrar todas as labels -->
    <v-dialog v-model="labelDialog" max-width="700px">
      <v-card>
        <v-card-title class="headline">
          Label Analysis
          <v-spacer></v-spacer>
          <v-btn icon @click="labelDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <div v-if="selectedItemLabels">
            <div class="mb-3">
              <strong>Text:</strong> {{ truncate(selectedItemText, 100) }}
            </div>

            <v-divider class="mb-4"></v-divider>

            <!-- Abas para alternar entre visualizações -->
            <v-tabs v-model="dialogTab" class="mb-4">
              <v-tab>Percentages</v-tab>
              <v-tab>User Votes</v-tab>
            </v-tabs>

            <v-tabs-items v-model="dialogTab">
              <!-- Aba de Percentagens -->
              <v-tab-item>
                <div v-for="(percentage, label) in selectedItemLabels" :key="label" class="label-percentage-dialog mb-3">
                  <div class="d-flex align-center mb-2">
                    <v-chip small :color="getLabelColor(label.toString())" class="mr-3 white--text">
                      {{ getLabelName(label.toString()) }}
                    </v-chip>
                    <span class="percentage-text-dialog">{{ percentage }}%</span>
                  </div>
                  <v-progress-linear
                    :value="percentage"
                    height="12"
                    :color="getLabelColor(label.toString())"
                    class="mb-1"
                  ></v-progress-linear>
                </div>
              </v-tab-item>

              <!-- Aba de Votos por Usuário -->
              <v-tab-item>
                <div v-if="selectedItemUserVotes && Object.keys(selectedItemUserVotes).length > 0">
                  <div v-for="(labelData, label) in selectedItemUserVotes" :key="label" class="mb-4">
                    <div class="d-flex align-center mb-2">
                      <v-chip small :color="getLabelColor(label.toString())" class="mr-3 white--text">
                        {{ getLabelName(label.toString()) }}
                      </v-chip>
                      <span class="caption">({{ labelData.users.length }} vote{{ labelData.users.length !== 1 ? 's' : '' }})</span>
                    </div>

                    <div class="ml-4">
                      <v-chip
                        v-for="user in labelData.users"
                        :key="user.id"
                        x-small
                        outlined
                        class="mr-1 mb-1"
                      >
                        <v-icon left x-small>mdi-account</v-icon>
                        {{ user.name }}
                      </v-chip>
                    </div>
                  </div>

                  <v-divider class="my-3"></v-divider>

                  <!-- Resumo -->
                  <div class="caption grey--text">
                    <strong>Summary:</strong>
                    {{ Object.keys(selectedItemUserVotes).length }} different label{{ Object.keys(selectedItemUserVotes).length !== 1 ? 's' : '' }}
                    from {{ getTotalVoters() }} user{{ getTotalVoters() !== 1 ? 's' : '' }}
                  </div>
                </div>

                <!-- Mensagem quando não há dados -->
                <div v-else class="text-center py-4">
                  <v-icon large color="grey">mdi-information-outline</v-icon>
                  <div class="mt-2 grey--text">
                    No user vote data available for this text.
                  </div>
                  <div class="caption grey--text mt-1">
                    Debug info: selectedItemUserVotes = {{ selectedItemUserVotes }}
                  </div>
                </div>
              </v-tab-item>
            </v-tabs-items>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="labelDialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script lang="ts">
import Vue from 'vue'
import { mdiMagnify, mdiAlertCircle } from '@mdi/js'
import type { PropType } from 'vue'

type ExampleDTO = {
  id: number
  text: string
  assignments?: Array<{
    id: string
    assignee: string
    assignee_id: number
  }>
  annotations: Array<{
    user: number
    label: string
    start_offset: number
    end_offset: number
  }>
}


export default Vue.extend({
  name: 'DiscrepancyList',
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
    }
  },

  data() {
    return {
      search: '',
      mdiMagnify,
      mdiAlertCircle,
      memberNames: {} as { [key: number]: string },
      showOnlyDiscrepancies: false,
      labelDialog: false,
      selectedItemLabels: null as { [label: string]: number } | null,
      selectedItemText: '',
      selectedItemUserVotes: null as { [label: string]: { users: Array<{ id: number, name: string }> } } | null,
      dialogTab: 0
    }
  },

  computed: {
    headers() {
      return [
        { text: 'Text', value: 'text', sortable: true },
        { text: 'Label Percentage', value: 'labelPercentages', sortable: false },
        { text: 'Participation', value: 'participation', sortable: false },
        { text: 'Discrepancy', value: 'discrepancyPercentage', sortable: true },
        { text: 'Status', value: 'status', sortable: false },
        { text: 'Action', value: 'action', sortable: false }
      ]
    },
    projectId(): string {
      return this.$route.params.id
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
    participationCount: number
    totalMembers: number
    participationRate: number
    discrepancyPercentage: number
    discrepancyData: { agreement: number, disagreement: number }
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

    // Encontrar o documento correspondente
    const item = this.items.find(i => i.id === docId)
    if (!item) return

    // Filtrar apenas usuários que estão atualmente assignados a este texto
    const exampleAssignees = item.assignments ? item.assignments.map((a: any) => a.assignee_id) : []
    const allMemberIds = Object.keys(annotations).map(id => parseInt(id))
    const memberIds = allMemberIds.filter(memberId => exampleAssignees.includes(memberId))

    if (memberIds.length <= 1) return

    let hasDiscrepancy = false
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
          hasDiscrepancy = true
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

    if (this.showOnlyDiscrepancies && !hasDiscrepancy) return

    // Calcular porcentagens de labels apenas para usuários assignados
    const labelCounts: { [label: string]: number } = {}
    const totalAnnotations: { [label: string]: number } = {}

    // Contar ocorrências de cada label apenas dos usuários assignados
    memberIds.forEach(memberId => {
      const memberAnnotations = annotations[memberId]
      if (memberAnnotations) {
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
      }
    })
    
    // Calcular porcentagens
    const labelPercentages: { [label: string]: number } = {}
    const totalLabels = Object.values(totalAnnotations).reduce((sum, count) => sum + count, 0)
    
    if (totalLabels > 0) {
      Object.keys(labelCounts).forEach(label => {
        labelPercentages[label] = Math.round((labelCounts[label] / totalLabels) * 100)
      })
    }
    
    // Calcular taxa de participação baseada nos assignees específicos deste exemplo
    const totalAssigneesForExample = exampleAssignees.length
    const participationCount = memberIds.length
    const participationRate = totalAssigneesForExample > 0 ? Math.round((participationCount / totalAssigneesForExample) * 100) : 0

    // Calcular percentagem de discrepância baseada no consenso real
    const labelVotes: { [label: string]: number } = {}
    let totalVotes = 0

    // Contar votos para cada label
    memberIds.forEach(memberId => {
      const memberAnnotations = annotations[memberId]
      if (memberAnnotations) {
        memberAnnotations.forEach((annotation: any) => {
          if (annotation.label) {
            const labelKey = annotation.label.toString()
            labelVotes[labelKey] = (labelVotes[labelKey] || 0) + 1
            totalVotes++
          }
        })
      }
    })

    // Calcular consenso real: apenas votos que concordam entre si
    let consensusVotes = 0

    // Para cada label, contar apenas os votos que concordam (mesmo label)
    Object.values(labelVotes).forEach(votes => {
      if (votes > 1) {
        // Se uma label tem mais de 1 voto, esses votos concordam entre si
        consensusVotes += votes
      }
    })

    const agreementPercentage = totalVotes > 0 ? Math.round((consensusVotes / totalVotes) * 100) : 0
    const discrepancyPercentage = 100 - agreementPercentage

    const discrepancyData = {
      agreement: agreementPercentage,
      disagreement: discrepancyPercentage
    }

    result.push({
      id: docId,
      text: item.text,
      annotationsText,
      hasDiscrepancy,
      discrepancyDetails,
      labelPercentages,
      participationCount,
      totalMembers: totalAssigneesForExample,
      participationRate,
      discrepancyPercentage,
      discrepancyData
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
    
    getParticipationColor(rate: number): string {
      if (rate < 30) return 'error'
      if (rate < 60) return 'warning'
      return 'success'
    },

    getDiscrepancyColor(percentage: number): string {
      if (percentage >= 70) return 'error'
      if (percentage >= 40) return 'warning'
      return 'success'
    },

    getRowClass(item: any): string {
      const discrepancyPercentage = item.discrepancyPercentage || 0
      if (discrepancyPercentage >= 70) return 'high-discrepancy-row'
      if (discrepancyPercentage >= 40) return 'medium-discrepancy-row'
      return 'low-discrepancy-row'
    },

    openLabelDialog(item: any) {
      this.selectedItemLabels = item.labelPercentages
      this.selectedItemText = item.text
      this.selectedItemUserVotes = this.getUserVotesForItem(item.id)
      this.dialogTab = 0
      this.labelDialog = true
    },

    getUserVotesForItem(itemId: number) {
      console.log('🔍 Getting user votes for item:', itemId)
      const userVotes: { [label: string]: { users: Array<{ id: number, name: string }> } } = {}

      // Encontrar o item específico
      const item = this.items.find(i => i.id === itemId)
      console.log('📄 Found item:', item)

      if (!item || !item.annotations) {
        console.log('❌ No item or annotations found')
        return null
      }

      // Filtrar apenas usuários assignados
      const exampleAssignees = item.assignments ? item.assignments.map((a: any) => a.assignee_id) : []
      console.log('👥 Example assignees:', exampleAssignees)
      console.log('📝 Item annotations:', item.annotations)

      // Agrupar anotações por label
      item.annotations.forEach((annotation: any) => {
        const userId = annotation.user ?? annotation.user_id ?? annotation.created_by
        console.log('🔍 Processing annotation:', annotation, 'userId:', userId)

        // Só considerar usuários assignados
        if (userId && exampleAssignees.includes(userId) && annotation.label) {
          const labelKey = annotation.label.toString()
          const userName = this.getUserName(userId)

          console.log('✅ Adding vote:', labelKey, 'by', userName)

          if (!userVotes[labelKey]) {
            userVotes[labelKey] = { users: [] }
          }

          // Evitar duplicatas do mesmo usuário
          if (!userVotes[labelKey].users.find(u => u.id === userId)) {
            userVotes[labelKey].users.push({
              id: userId,
              name: userName
            })
          }
        } else {
          console.log('❌ Skipping annotation - userId:', userId, 'assignees:', exampleAssignees, 'label:', annotation.label)
        }
      })

      console.log('📊 Final user votes:', userVotes)
      return userVotes
    },

    getTotalVoters(): number {
      if (!this.selectedItemUserVotes) return 0

      const allUsers = new Set<number>()
      Object.values(this.selectedItemUserVotes).forEach(labelData => {
        labelData.users.forEach(user => allUsers.add(user.id))
      })

      return allUsers.size
    },

    getUserName(userId: number): string {
      // Primeiro, tentar buscar no memberNames (cache)
      if (this.memberNames[userId]) {
        return this.memberNames[userId]
      }

      // Segundo, buscar na lista de members passada como prop
      const member = this.members.find((m: any) => m.user === userId || m.id === userId)
      if (member) {
        const username = member.username || member.user_name || member.name
        // Cachear para uso futuro
        this.$set(this.memberNames, userId, username)
        return username
      }

      // Terceiro, buscar nos assignments dos items para pegar o nome
      for (const item of this.items) {
        if (item.assignments) {
          const assignment = item.assignments.find((a: any) => a.assignee_id === userId)
          if (assignment && assignment.assignee) {
            const username = assignment.assignee
            this.$set(this.memberNames, userId, username)
            return username
          }
        }
      }

      // Fallback para User ID
      return `User ${userId}`
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
      console.log('📋 Loading member names. Members prop:', this.members)

      // Usar os dados dos members que já foram buscados na página principal
      this.members.forEach((member: any) => {
        const userId = member.user || member.id
        const username = member.username || member.user_name || member.name
        if (userId && username) {
          this.$set(this.memberNames, userId, username)
          console.log('✅ Loaded member:', userId, '->', username)
        }
      })

      // Carregar nomes dos assignments também
      this.items.forEach(item => {
        if (item.assignments && Array.isArray(item.assignments)) {
          item.assignments.forEach((assignment: any) => {
            const userId = assignment.assignee_id
            const username = assignment.assignee
            if (userId && username && !this.memberNames[userId]) {
              this.$set(this.memberNames, userId, username)
              console.log('✅ Loaded from assignment:', userId, '->', username)
            }
          })
        }
      })

      // Para qualquer member ID que não esteja na lista, usar um fallback
      const memberIds = new Set<number>()
      this.items.forEach(item => {
        if (item.annotations && Array.isArray(item.annotations)) {
          item.annotations.forEach((annotation: any) => {
            const userId = annotation.user ?? annotation.user_id ?? annotation.created_by
            if (userId && !this.memberNames[userId]) {
              memberIds.add(userId)
            }
          })
        }
      })

      // Só buscar members que não estão na lista já carregada
      memberIds.forEach(memberId => {
        if (!this.memberNames[memberId]) {
          this.$set(this.memberNames, memberId, `User ${memberId}`)
          console.log('⚠️ Fallback for user:', memberId)
        }
      })

      console.log('📋 Final memberNames:', this.memberNames)
    },

    viewAnnotation(item: any) {
      console.log('🔍 ViewAnnotation called with item:', item)

      // Buscar o item original com assignments
      const originalItem = this.items.find(i => i.id === item.id)
      console.log('📄 Original item found:', originalItem)

      // Verificar se o usuário atual está assignado a este texto
      const currentUserId = this.$store.getters['auth/getUserId']
      console.log('👤 Current user ID:', currentUserId)

      const assignments = originalItem?.assignments || item.assignments
      console.log('📋 Assignments:', assignments)

      const isAssignee = assignments && assignments.some((assignment: any) => assignment.assignee_id === currentUserId)
      console.log('✅ Is assignee:', isAssignee)

      if (!isAssignee) {
        // Mostrar erro se não estiver assignado
        console.log('❌ User not assigned, showing error')
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: this.$t('dataset.notAssigneeError')
        })
        return
      }

      // Se estiver assignado, prosseguir normalmente
      console.log('✅ User is assigned, proceeding to annotation page')
      const link = this.getLinkToAnnotationPage()
      console.log('🔗 Navigation link:', link)

      this.$router.push({
        path: this.$nuxt.localePath(link),
        query: { page: item.id.toString() }
      })
    },

    getLinkToAnnotationPage() {
      const projectType = this.$store.getters['projects/project'].projectType
      const projectId = this.projectId
      const mapping: { [key: string]: string } = {
        'DocumentClassification': `/projects/${projectId}/text-classification`,
        'SequenceLabeling': `/projects/${projectId}/sequence-labeling`,
        'Seq2seq': `/projects/${projectId}/sequence-to-sequence`,
        'ImageClassification': `/projects/${projectId}/image-classification`,
        'Speech2text': `/projects/${projectId}/speech-to-text`,
        'ImageCaptioning': `/projects/${projectId}/image-captioning`,
        'IntentDetectionAndSlotFilling': `/projects/${projectId}/intent-detection-and-slot-filling`,
        'BoundingBox': `/projects/${projectId}/object-detection`,
        'Segmentation': `/projects/${projectId}/segmentation`
      }
      return mapping[projectType] || `/projects/${projectId}`
    }
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


.participation-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.discrepancy-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* Classes para colorir as linhas baseadas na discrepância */
::v-deep .high-discrepancy-row {
  background-color: rgba(244, 67, 54, 0.1) !important;
}

::v-deep .medium-discrepancy-row {
  background-color: rgba(255, 152, 0, 0.1) !important;
}

::v-deep .low-discrepancy-row {
  background-color: rgba(76, 175, 80, 0.05) !important;
}

/* Estilos para o dialog de labels */
.label-percentage-dialog {
  margin-bottom: 16px;
}

.percentage-text-dialog {
  font-weight: bold;
  font-size: 14px;
  min-width: 40px;
}
</style>
