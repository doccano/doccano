<template>
  <v-card>
    <v-card-title>
      <h2>Discrepancies</h2>
      <v-spacer />
    </v-card-title>
    <v-card-text>
      <DiscrepancyList
        :items="items"
        :is-loading="isLoading"
        :members="members"
      />
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'
import DiscrepancyList from '../../../../components/discrepancy/DiscrepancyList.vue'

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
  name: 'DiscrepancyPage',

  components: {
    DiscrepancyList
  },

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
      this.$store.commit('projects/setPageTitle', 'Discrepâncias entre Anotações')
    }
  }
})
</script>