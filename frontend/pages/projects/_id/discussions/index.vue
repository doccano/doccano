<template>
  <v-container class="pt-16">

    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <h2>📋 Discussões em aberto</h2>
        <v-btn color="primary" @click="showCreateDialog = true">
          ➕ Criar nova discussão
        </v-btn>
      </v-col>

      <!-- Mensagem de fallback -->
      <v-col v-if="openDiscussions.length === 0 && !showCreateDialog" cols="12">
        <v-alert type="info" text>
          Nenhuma discussão em aberto.
        </v-alert>
      </v-col>

      <!-- Tabela de discussões em aberto -->
      <v-col v-if="openDiscussions.length > 0" cols="12">
        <v-data-table
          :headers="headers"
          :items="openDiscussions"
          :items-per-page="10"
          class="elevation-1"
        >
          <template #item="{ item }">
            <tr>
              <td>{{ item.title }}</td>
              <td>{{ formatDate(item.start_date) }} → {{ formatDate(item.end_date) }}</td>
              <td class="text-center">
                <v-btn
                  color="primary"
                  small
                  @click="goToDiscussion(item.id)"
                >
                  Discutir
                </v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>

      <!-- Alternador para discussões encerradas -->
      <v-col v-if="isProjectAdmin" cols="12">
        <v-btn text @click="showClosed = !showClosed">
          {{ showClosed ? '🔼 Ocultar' : '📁 Ver discussões encerradas' }}
        </v-btn>
      </v-col>

      <!-- Tabela de discussões encerradas -->
      <v-col v-if="showClosed && closedDiscussions.length > 0" cols="12">
        <v-data-table
          :headers="headers"
          :items="closedDiscussions"
          :items-per-page="5"
          class="elevation-1 grey lighten-4"
        >
          <template #item="{ item }">
            <tr>
              <td>{{ item.title }}</td>
              <td>{{ formatDate(item.start_date) }} → {{ formatDate(item.end_date) }}</td>
              <td class="text-center">
                <v-btn
                  color="secondary"
                  small
                  @click="goToDiscussion(item.id)"
                >
                  Visualizar
                </v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- Modal de criação de discussão -->
    <v-dialog v-model="showCreateDialog" max-width="500px">
      <v-card>
        <v-card-title>Criar nova discussão</v-card-title>
        <v-card-text>
          <v-text-field v-model="newDiscussion.title" label="Título" />

          <v-menu v-model="menu1" :close-on-content-click="false" transition="scale-transition">
            <template #activator="{ on, attrs }">
              <v-text-field
                v-model="newDiscussion.start_date"
                label="Início"
                readonly
                v-bind="attrs"
                v-on="on"
              />
            </template>
            <v-date-picker v-model="newDiscussion.start_date" @input="menu1 = false" />
          </v-menu>

          <v-menu v-model="menu2" :close-on-content-click="false" transition="scale-transition">
            <template #activator="{ on, attrs }">
              <v-text-field
                v-model="newDiscussion.end_date"
                label="Fim"
                readonly
                v-bind="attrs"
                v-on="on"
              />
            </template>
            <v-date-picker v-model="newDiscussion.end_date" @input="menu2 = false" />
          </v-menu>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showCreateDialog = false">Cancelar</v-btn>
          <v-btn color="primary" @click="createDiscussion">Criar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar para notificações -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      top
    >
      {{ snackbar.text }}
      <template #action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar.show = false">
          Fechar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>


<script lang="ts">
export default {
  name: 'DiscussionListPage',
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      discussions: [] as any[],
      showClosed: false,
      showCreateDialog: false,
      newDiscussion: {
        title: '',
        start_date: new Date().toISOString().substr(0, 10),
        end_date: ''
      },
      menu1: false,
      menu2: false,
      isProjectAdmin: false,
      headers: [
        { text: 'Título', value: 'title', sortable: true },
        { text: 'Período', value: 'dates', sortable: false },
        { text: 'Ações', value: 'actions', sortable: false, align: 'center' }
      ],
      // Adicionando estado para controlar a notificação
      snackbar: {
        show: false,
        text: '',
        color: 'success',
        timeout: 3000
      }
    }
  },

  async fetch() {
    try {
      const res = await this.$axios.get(`/v1/projects/${this.projectId}/discussions/`)
      this.discussions = Array.isArray(res.data?.results) ? res.data.results : []

      
      // Buscar informação se o usuário é admin do projeto
      const member = await this.$repositories.member.fetchMyRole(this.projectId)
      this.isProjectAdmin = member.isProjectAdmin
    } catch (err) {
      console.error('Erro ao carregar discussões:', err)
      this.discussions = []
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },
    openDiscussions() {
      if (!Array.isArray(this.discussions)) return []
      const now = new Date()
      return this.discussions.filter(d => new Date(d.end_date) >= now)
    },
    closedDiscussions() {
      if (!Array.isArray(this.discussions)) return []
      const now = new Date()
      return this.discussions.filter(d => new Date(d.end_date) < now)
    }
  },

  mounted() {
    console.log('🟢 Página de discussões carregada. Projeto ID:', this.projectId)
    // Definir uma data de fim padrão (7 dias a partir de hoje)
    const defaultEndDate = new Date()
    defaultEndDate.setDate(defaultEndDate.getDate() + 7)
    this.newDiscussion.end_date = defaultEndDate.toISOString().substr(0, 10)
  },

  methods: {
    formatDate(date: string): string {
      return new Date(date).toLocaleDateString('pt-PT')
    },

    async createDiscussion() {
      if (!this.newDiscussion.title) {
        alert('Por favor, informe um título para a discussão')
        return
      }

      try {
        const res = await this.$axios.post(`/v1/projects/${this.projectId}/discussions/`, this.newDiscussion)
        this.discussions.push(res.data)
        this.showCreateDialog = false
        
        // Não redirecionar mais para a discussão, apenas mostrar mensagem de sucesso
        this.snackbar = {
          show: true,
          text: 'Discussão criada com sucesso!',
          color: 'success',
          timeout: 3000
        }
        
        // Limpar o formulário para próxima criação
        this.newDiscussion = {
          title: '',
          start_date: new Date().toISOString().substr(0, 10),
          end_date: ''
        }
        
        // Definir data de fim padrão (7 dias a partir de hoje)
        const defaultEndDate = new Date()
        defaultEndDate.setDate(defaultEndDate.getDate() + 7)
        this.newDiscussion.end_date = defaultEndDate.toISOString().substr(0, 10)
      } catch (err) {
        console.error('Erro ao criar discussão:', err)
        this.snackbar = {
          show: true,
          text: 'Erro ao criar discussão. Tente novamente.',
          color: 'error',
          timeout: 3000
        }
      }
    },

    goToDiscussion(id: number) {
      this.$router.push(`/projects/${this.projectId}/discussions/${id}`)
    }
  }
}
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
