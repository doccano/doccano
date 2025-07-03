<template>
  <v-card>
    <v-card-title>
      <h2>Compare Annotations</h2>
      <v-spacer />
    </v-card-title>
    
    <v-card-text>
      <!-- Filtro para seleção de usuários -->
      <v-row class="mb-4">
        <v-col cols="12" md="6">
          <v-select
            v-model="selectedUsers"
            :items="availableUsers"
            item-text="username"
            item-value="id"
            label="Select Users to Compare"
            multiple
            chips
            small-chips
            deletable-chips
            outlined
            :rules="[v => !v || v.length >= 2 || 'Select at least 2 users', v => !v || v.length <= 5 || 'Select maximum 5 users']"
          >
            <template #selection="{ item, index }">
              <v-chip
                v-if="index < 3"
                :key="item.id"
                color="primary"
                small
                close
                @click:close="removeUser(item.id)"
              >
                {{ item.username }}
              </v-chip>
              <span
                v-if="index === 3"
                :key="item.id"
                class="grey--text caption"
              >
                (+{{ selectedUsers.length - 3 }} others)
              </span>
            </template>
          </v-select>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="search"
            prepend-inner-icon="mdi-magnify"
            label="Search text..."
            outlined
            hide-details
            clearable
          />
        </v-col>
      </v-row>

      <!-- Tabela de comparação -->
      <v-data-table
        :items="processedItems"
        :headers="dynamicHeaders"
        :loading="isLoading"
                 :search="search"
         loading-text="Loading comparison data..."
         :no-data-text="noDataMessage"
        :footer-props="{
          showFirstLastPage: true,
          'items-per-page-options': [10, 25, 50, 100],
          'items-per-page-text': 'Items per page:',
          'page-text': '{0}-{1} of {2}'
        }"
        item-key="id"
        :item-class="getRowClass"
      >
        <!-- Template para texto (primeira coluna) -->
        <template #[`item.text`]="{ item }">
          <div class="text-truncate" style="max-width: 300px;">
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on">
                  {{ truncateText(item.text, 100) }}
                </span>
              </template>
              <span>{{ item.text }}</span>
            </v-tooltip>
          </div>
        </template>

        <!-- Templates dinâmicos para colunas de usuários -->
        <template v-for="user in selectedUsers" #[`item.user_${user}`]="{ item }">
          <div :key="`user_${user}`">
            <v-chip
              v-for="label in item.userAnnotations[user] || []"
              :key="`${user}_${label}`"
              small
              :color="getLabelColor(label)"
              text-color="white"
              class="ma-1"
            >
              {{ label }}
            </v-chip>
            <span v-if="!item.userAnnotations[user] || item.userAnnotations[user].length === 0" class="grey--text">
              No annotation
            </span>
          </div>
        </template>

        <!-- Template para coluna de discrepância -->
        <template #[`item.discrepancy`]="{ item }">
          <v-chip
            :color="getDiscrepancyColor(item.discrepancyStatus)"
            text-color="white"
            small
          >
            <v-icon left small>
              {{ getDiscrepancyIcon(item.discrepancyStatus) }}
            </v-icon>
            {{ getDiscrepancyText(item.discrepancyStatus) }}
          </v-chip>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'

type UserAnnotation = {
  id: number
  username: string
}

type ExampleItem = {
  id: number
  text: string
  userAnnotations: { [userId: number]: string[] }
  hasDiscrepancy: boolean
  discrepancyStatus: 'agreement' | 'discrepancy' | 'no_annotations'
}

export default Vue.extend({
  name: 'CompareAnnotations',
  
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      isLoading: true,
      selectedUsers: [] as number[],
      availableUsers: [] as UserAnnotation[],
      examples: [] as any[],
      search: '' as string,
      labelColors: {} as { [label: string]: string }
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      const projectId = this.$route.params.id

      // Buscar membros do projeto
      const membersResponse = await this.$repositories.member.list(projectId)
      this.availableUsers = membersResponse.map((member: any) => ({
        id: member.user,
        username: member.username
      }))

      // Buscar exemplos com anotações
      await this.loadExamples()

      // Auto-selecionar os primeiros 2 usuários se disponíveis (para facilitar teste)
      if (this.availableUsers.length >= 2) {
        this.selectedUsers = [this.availableUsers[0].id, this.availableUsers[1].id]
        console.log('🎯 Auto-selected users:', this.selectedUsers)
      }

      console.log('✅ Loaded', this.availableUsers.length, 'users and', this.examples.length, 'examples')

    } catch (error) {
      console.error('Error loading comparison data:', error)
    } finally {
      this.isLoading = false
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    
    dynamicHeaders() {
      const headers = [
        { text: 'Text', value: 'text', sortable: true, width: '300px' }
      ]
      
      // Adicionar colunas para cada usuário selecionado
      this.selectedUsers.forEach(userId => {
        const user = this.availableUsers.find(u => u.id === userId)
        if (user) {
          headers.push({
            text: user.username,
            value: `user_${userId}`,
            sortable: false,
            width: '200px'
          })
        }
      })
      
              // Adicionar coluna de discrepância
        if (this.selectedUsers.length >= 2) {
          headers.push({
            text: 'Consensus',
            value: 'discrepancy',
            sortable: true,
            width: '150px'
          })
        }
      
      return headers
    },

    processedItems(): ExampleItem[] {
      if (this.selectedUsers.length < 2) {
        return []
      }

      const processed = this.examples
        .map(example => {
          const userAnnotations: { [userId: number]: string[] } = {}
          
          // Processar anotações por usuário
          this.selectedUsers.forEach(userId => {
            userAnnotations[userId] = this.getUserAnnotations(example, userId)
          })

          // Verificar se algum usuário selecionado fez anotações
          const hasAnyAnnotations = this.selectedUsers.some(userId => 
            userAnnotations[userId] && userAnnotations[userId].length > 0
          )

          // Se nenhum usuário selecionado anotou, pular este exemplo
          if (!hasAnyAnnotations) {
            return null
          }

          // Verificar discrepâncias e determinar status
          const discrepancyResult = this.checkDiscrepancyWithStatus(userAnnotations)

          return {
            id: example.id,
            text: example.text,
            userAnnotations,
            hasDiscrepancy: discrepancyResult.hasDiscrepancy,
            discrepancyStatus: discrepancyResult.status
          }
        })
        .filter(item => item !== null) as ExampleItem[] // Remover itens nulos
      
      console.log('✅ Processed', processed.length, 'examples with relevant annotations for', this.selectedUsers.length, 'users')
      return processed
    },

    noDataMessage() {
      if (this.selectedUsers.length < 2) {
        return 'Please select at least 2 users to compare annotations'
      }
      if (this.examples.length === 0) {
        return 'No examples found in this project'
      }
      return 'No examples found where the selected users have made annotations. Try selecting different users or check if they have annotated any examples.'
    }
  },

  methods: {
    async loadExamples() {
      try {
        const projectId = this.$route.params.id
        
        // Usar a mesma abordagem EXATA da página de discrepâncias
        const response = await this.$repositories.example.list(projectId, {
          limit: '1000',
          offset: '0',
          include_annotation: 'true'  // CHAVE PARA INCLUIR ANOTAÇÕES!
        })
        
        // Processar da mesma forma que a página de discrepâncias
        this.examples = response.items.map((item: any) => {
          return {
            id: item.id,
            text: item.text,
            assignments: item.assignments || [],
            annotations: (item.annotations || []).map((a: any) => ({
              user: a.user ?? a.user_id ?? a.created_by,
              label: a.label,
              start_offset: a.start_offset,
              end_offset: a.end_offset,
              text: a.text,
              type: a.type
            }))
          }
        })
        
        console.log('📄 Loaded', this.examples.length, 'examples with annotations')
        
      } catch (error) {
        console.error('Error loading examples:', error)
        this.examples = []
      }
    },

    getUserAnnotations(example: any, userId: number): string[] {
      if (!example.annotations) {
        return []
      }
      
      const userAnnotations = example.annotations
        .filter((annotation: any) => {
          const annotationUserId = annotation.user || annotation.user_id || annotation.created_by
          return annotationUserId === userId
        })
        .map((annotation: any) => annotation.label || 'Unlabeled')
        .filter((label: string, index: number, self: string[]) => self.indexOf(label) === index) // Remove duplicates
      
      return userAnnotations
    },

    checkDiscrepancyWithStatus(userAnnotations: { [userId: number]: string[] }): { hasDiscrepancy: boolean, status: 'agreement' | 'discrepancy' | 'no_annotations' } {
      const userIds = Object.keys(userAnnotations).map(id => parseInt(id))
      
      // Verificar quantos usuários têm anotações
      const usersWithAnnotations = userIds.filter(userId => 
        userAnnotations[userId] && userAnnotations[userId].length > 0
      )

      // Se menos de 2 usuários anotaram, é neutro
      if (usersWithAnnotations.length < 2) {
        return { hasDiscrepancy: false, status: 'no_annotations' }
      }

      // Comparar as anotações dos usuários que anotaram
      const firstUserAnnotations = userAnnotations[usersWithAnnotations[0]]
      
      for (let i = 1; i < usersWithAnnotations.length; i++) {
        const currentUserAnnotations = userAnnotations[usersWithAnnotations[i]]
        
        // Verificar se as anotações são diferentes
        if (!this.arraysEqual(firstUserAnnotations, currentUserAnnotations)) {
          return { hasDiscrepancy: true, status: 'discrepancy' }
        }
      }
      
      return { hasDiscrepancy: false, status: 'agreement' }
    },

    arraysEqual(arr1: string[], arr2: string[]): boolean {
      if (arr1.length !== arr2.length) return false
      
      const sorted1 = [...arr1].sort()
      const sorted2 = [...arr2].sort()
      
      return sorted1.every((val, index) => val === sorted2[index])
    },

    removeUser(userId: number) {
      this.selectedUsers = this.selectedUsers.filter(id => id !== userId)
    },

    truncateText(text: string, length: number): string {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    },

    getLabelColor(label: string): string {
      if (!this.labelColors[label]) {
        // Gerar uma cor consistente para cada label
        const colors = ['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success']
        const hash = this.hashString(label)
        this.labelColors[label] = colors[hash % colors.length]
      }
      return this.labelColors[label]
    },

    hashString(str: string): number {
      let hash = 0
      for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i)
        hash = ((hash << 5) - hash) + char
        hash = hash & hash // Convert to 32bit integer
      }
      return Math.abs(hash)
    },

    getRowClass(item: ExampleItem): string {
      return item.hasDiscrepancy ? 'discrepancy-row' : ''
    },

    getDiscrepancyColor(status: 'agreement' | 'discrepancy' | 'no_annotations'): string {
      switch (status) {
        case 'agreement': return 'success'
        case 'discrepancy': return 'error' 
        case 'no_annotations': return 'grey'
        default: return 'grey'
      }
    },

    getDiscrepancyIcon(status: 'agreement' | 'discrepancy' | 'no_annotations'): string {
      switch (status) {
        case 'agreement': return 'mdi-check-circle'
        case 'discrepancy': return 'mdi-alert-circle'
        case 'no_annotations': return 'mdi-minus-circle'
        default: return 'mdi-minus-circle'
      }
    },

    getDiscrepancyText(status: 'agreement' | 'discrepancy' | 'no_annotations'): string {
      switch (status) {
        case 'agreement': return 'Agreement'
        case 'discrepancy': return 'Disagreement'
        case 'no_annotations': return 'Insufficient Data'
        default: return 'Unknown'
      }
    }
  }
})
</script>

<style scoped>
.discrepancy-row {
  background-color: #fff3e0 !important;
}

.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style> 