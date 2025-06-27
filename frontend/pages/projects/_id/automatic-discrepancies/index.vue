<template>
  <v-card>
    <v-card-title>
      <h2>Automatic Discrepancies</h2>
      <v-spacer />
      <v-card 
        color="gradient" 
        class="pa-3 ml-4 d-flex align-center" 
        style="background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); border-radius: 12px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);"
        elevation="0"
      >
        <v-icon color="white" class="mr-2">mdi-target</v-icon>
        <div class="white--text">
          <div class="text-caption font-weight-medium opacity-90">Threshold</div>
          <div class="text-h6 font-weight-bold">{{ $store.getters['projects/project'].labelDiscrepancyThreshold }}%</div>
        </div>
      </v-card>
    </v-card-title>
    <v-card-text>
      <!-- Mensagem de erro da base de dados -->
      <v-alert
        v-if="!isDatabaseHealthy"
        type="error"
        class="mb-4"
      >
        De momento, a base de dados não se encontra disponível. Por favor, tente mais tarde.
      </v-alert>

      <AutomaticDiscrepancyList
        :items="items"
        :is-loading="isDatabaseHealthy && isLoading"
        :members="members"
        :database-error="!isDatabaseHealthy"
      />
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import AutomaticDiscrepancyList from '../../../../components/discrepancy/AutomaticDiscrepancyList.vue'
import { databaseHealthMixin } from '../../../../mixins/databaseHealthMixin'

// Definindo o tipo localmente para evitar import quebrado
export type ExampleDTO = {
  id: number
  text: string
  annotations: Array<{
    user: number
    label: string
    start_offset: number
    end_offset: number
  }>
}

export type MemberItem = {
  id: number
  username: string
}

export default defineComponent({
  name: 'AutomaticDiscrepancyPage',

  components: {
    AutomaticDiscrepancyList
  },

  mixins: [databaseHealthMixin],

  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      items: [] as ExampleDTO[],
      members: [] as MemberItem[],
      isLoading: false
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    projectId(): string {
      return this.$route.params.id
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      const [examplesResponse, membersResponse] = await Promise.all([
        this.$repositories.example.list(this.projectId, {
          limit: '1000',
          offset: '0',
          include_annotation: 'true'
        }),
        this.$repositories.member.list(this.projectId)
      ])

      this.items = examplesResponse.items.map((item: any) => {
        return {
          id: item.id,
          text: item.text,
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

      this.members = membersResponse.map((member: any) => ({
        id: member.id,
        username: member.username
      }))

      console.log('📦 Anotações recebidas:', JSON.stringify(this.items, null, 2))
    } catch (e) {
      console.error('Erro ao buscar dados do projeto:', e)
    } finally {
      this.isLoading = false
    }
  },

  mounted() {
    if (this.$store.hasModule('projects')) {
      this.$store.commit('projects/setPageTitle', 'Discrepâncias Automáticas entre Anotações')
    }
  }
})
</script>