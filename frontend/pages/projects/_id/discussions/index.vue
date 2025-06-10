<template>
  <v-container class="pt-16">
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <h2>📋 Discussions</h2>
        <v-btn v-if="isProjectAdmin" color="primary" @click="showCreateDialog = true">
          ➕ Create new discussion
        </v-btn>
      </v-col>

      <v-col v-if="openDiscussions.length > 0" cols="12" class="mt-4">
        <h3>Open</h3>
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
                <v-btn color="primary" small class="mx-2" @click="goToDiscussion(item.id)">Discuss</v-btn>
                <v-btn v-if="isProjectAdmin" color="orange" dark small class="mx-2" @click="confirmClose(item)">Close</v-btn>
                <v-btn v-if="isProjectAdmin" text small color="primary" class="mx-2" @click="openEditDialog(item)">Edit</v-btn>
                <v-btn v-if="isProjectAdmin" text small color="error" class="mx-2" @click="confirmDelete(item)">Delete</v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>

      <v-col v-if="futureDiscussions.length > 0" cols="12" class="mt-4">
        <h3>📅 Upcoming</h3>
        <v-data-table
          :headers="headers"
          :items="futureDiscussions"
          :items-per-page="5"
          class="elevation-1"
        >
          <template #item="{ item }">
            <tr>
              <td>{{ item.title }}</td>
              <td>{{ formatDate(item.start_date) }} → {{ formatDate(item.end_date) }}</td>
              <td class="text-center">
                <v-btn v-if="isProjectAdmin" text small color="primary" class="mx-2" @click="openEditDialog(item)">Edit</v-btn>
                <v-btn v-if="isProjectAdmin" text small color="error" class="mx-2" @click="confirmDelete(item)">Delete</v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>

      <v-col v-if="isProjectAdmin" cols="12" class="mt-4">
        <v-btn text @click="showClosed = !showClosed">
          {{ showClosed ? '🔼 Hide' : '📁 View closed discussions' }}
        </v-btn>
      </v-col>

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
                 <v-btn color="secondary" small class="mx-2" @click="goToDiscussion(item.id)">View</v-btn>
                 <v-btn v-if="isProjectAdmin" color="success" small class="mx-2" @click="confirmReopen(item)">Reopen</v-btn>
                 <v-btn text small color="primary" class="mx-2" @click="openEditDialog(item)">Edit</v-btn>
                 <v-btn v-if="isProjectAdmin" text small color="error" class="mx-2" @click="confirmDelete(item)">Delete</v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>

      <v-col v-if="!openDiscussions.length && !futureDiscussions.length && !showCreateDialog" cols="12">
         <v-alert type="info" text>
          No discussions scheduled. Create one to get started!
        </v-alert>
      </v-col>

    </v-row>

    <v-dialog v-model="showCreateDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title>Criate new discussion</v-card-title>
        <v-card-text>
          <v-text-field v-model="newDiscussion.title" label="Discussion name" />
          <v-menu v-model="menu1" :close-on-content-click="false" transition="scale-transition">
            <template #activator="{ on, attrs }">
              <v-text-field v-model="newDiscussion.start_date" label="Start date" readonly v-bind="attrs" v-on="on" />
            </template>
            <v-date-picker v-model="newDiscussion.start_date" @input="menu1 = false" />
          </v-menu>
          <v-menu v-model="menu2" :close-on-content-click="false" transition="scale-transition">
            <template #activator="{ on, attrs }">
              <v-text-field v-model="newDiscussion.end_date" label="End date" readonly v-bind="attrs" v-on="on" />
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

    <v-dialog v-model="showEditDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title>Edit Discussion</v-card-title>
        <v-card-text>
          <v-text-field v-model="editingDiscussion.title" label="Discussion Name" />
          <v-menu v-model="editMenu1" :close-on-content-click="false" transition="scale-transition">
            <template #activator="{ on, attrs }">
              <v-text-field v-model="editingDiscussion.start_date" label="Start date" readonly v-bind="attrs" v-on="on" />
            </template>
            <v-date-picker v-model="editingDiscussion.start_date" @input="editMenu1 = false" />
          </v-menu>
          <v-menu v-model="editMenu2" :close-on-content-click="false" transition="scale-transition">
            <template #activator="{ on, attrs }">
              <v-text-field v-model="editingDiscussion.end_date" label="End date" readonly v-bind="attrs" v-on="on" />
            </template>
            <v-date-picker v-model="editingDiscussion.end_date" @input="editMenu2 = false" />
          </v-menu>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showEditDialog = false">Cancelar</v-btn>
          <v-btn color="primary" @click="saveDiscussion">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showCloseDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title class="headline">Close Discussion?</v-card-title>
        <v-card-text class="body-1 mt-4">
          Are you sure you want to close the discussion <strong>"{{ selectedDiscussion?.title }}"</strong>?
          The end date will be set to today.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showCloseDialog = false">Cancelar</v-btn>
          <v-btn color="orange" dark @click="closeDiscussion">Encerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showDeleteDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title class="headline error--text">Delete Discussion?</v-card-title>
        <v-card-text>
          <p class="body-1 mt-4">
            Are you sure you want to permanently delete the discussion <strong>"{{ selectedDiscussion?.title }}"</strong>?
          </p>
          <p class="font-weight-bold">All chat messages will also be deleted and this action cannot be undone.</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteDiscussion">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showReopenDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title class="headline">Reopen discussion</v-card-title>
        <v-card-text>
          Select a new end date for the discussion
          <strong>"{{ selectedDiscussion?.title }}"</strong>:
          <v-menu v-model="reopenMenu" :close-on-content-click="false" transition="scale-transition">
            <template #activator="{ on, attrs }">
              <v-text-field v-model="newEndDate" label="New end date" readonly v-bind="attrs" v-on="on" />
            </template>
            <v-date-picker v-model="newEndDate" @input="reopenMenu = false" />
          </v-menu>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showReopenDialog = false">Cancelar</v-btn>
          <v-btn color="primary" @click="reopenDiscussion">Confirmar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout" top>
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
      showCloseDialog: false,
      showReopenDialog: false,
      showEditDialog: false,
      showDeleteDialog: false,
      reopenMenu: false,
      editMenu1: false,
      editMenu2: false,
      newEndDate: '',
      selectedDiscussion: null as any,
      newDiscussion: {
        title: '',
        start_date: new Date().toISOString().substr(0, 10),
        end_date: ''
      },
      editingDiscussion: {
        id: null,
        title: '',
        start_date: '',
        end_date: ''
      },
      menu1: false,
      menu2: false,
      isProjectAdmin: false,
      headers: [
        { text: 'Discussion Name', value: 'title', sortable: true },
        { text: 'Date', value: 'dates', sortable: false },
        { text: 'Actions', value: 'actions', sortable: false, align: 'center' }
      ],
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
    
    futureDiscussions() {
      const todayString = new Date().toISOString().substr(0, 10);
      return this.discussions.filter(d => d.start_date > todayString);
    },

    closedDiscussions() {
      const todayString = new Date().toISOString().substr(0, 10);
      return this.discussions.filter(d => d.end_date <= todayString);
    },

    openDiscussions() {
      const todayString = new Date().toISOString().substr(0, 10);
      return this.discussions.filter(d => 
        d.start_date <= todayString && d.end_date > todayString
      );
    }
  },

  mounted() {
    const defaultEndDate = new Date()
    defaultEndDate.setDate(defaultEndDate.getDate() + 7)
    this.newDiscussion.end_date = defaultEndDate.toISOString().substr(0, 10)
  },

  methods: {
    formatDate(dateString: string): string {
      if (!dateString) return '';
      const date = new Date(dateString + 'T00:00:00Z');
      return date.toLocaleDateString('pt-PT', {
        timeZone: 'UTC',
      });
    },

    async createDiscussion() {
      if (!this.newDiscussion.title) {
        alert('Por favor, informe um título para a discussão');
        return;
      }
      try {
        const res = await this.$axios.post(`/v1/projects/${this.projectId}/discussions/`, this.newDiscussion);
        this.discussions.push(res.data);
        this.showCreateDialog = false;
        this.snackbar = { show: true, text: 'Discussão criada com sucesso!', color: 'success', timeout: 3000 };
        
        const defaultEndDate = new Date();
        defaultEndDate.setDate(defaultEndDate.getDate() + 7);
        this.newDiscussion = {
          title: '',
          start_date: new Date().toISOString().substr(0, 10),
          end_date: defaultEndDate.toISOString().substr(0, 10)
        };
      } catch (err) {
        console.error('Erro ao criar discussão:', err);
        this.snackbar = { show: true, text: 'Erro ao criar discussão. Tente novamente.', color: 'error', timeout: 3000 };
      }
    },

    openEditDialog(item: any) {
      this.editingDiscussion = JSON.parse(JSON.stringify(item));
      this.showEditDialog = true;
    },

    async saveDiscussion() {
      if (!this.editingDiscussion.title) {
        alert('O título não pode ficar em branco.');
        return;
      }
      try {
        const res = await this.$axios.patch(
          `/v1/projects/${this.projectId}/discussions/${this.editingDiscussion.id}/`,
          this.editingDiscussion
        );
        const index = this.discussions.findIndex(d => d.id === this.editingDiscussion.id);
        if (index !== -1) {
          this.$set(this.discussions, index, res.data);
        }
        this.showEditDialog = false;
        this.snackbar = { show: true, text: 'Discussão atualizada com sucesso!', color: 'success', timeout: 3000 };
      } catch (err) {
        console.error('Erro ao atualizar discussão:', err);
        this.snackbar = { show: true, text: 'Erro ao atualizar discussão.', color: 'error', timeout: 3000 };
      }
    },

    confirmDelete(item: any) {
      this.selectedDiscussion = item;
      this.showDeleteDialog = true;
    },

    async deleteDiscussion() {
      if (!this.selectedDiscussion) return;
      try {
        await this.$axios.delete(
          `/v1/projects/${this.projectId}/discussions/${this.selectedDiscussion.id}/`
        );

        const index = this.discussions.findIndex(d => d.id === this.selectedDiscussion.id);
        if (index !== -1) {
          this.discussions.splice(index, 1);
        }

        this.showDeleteDialog = false;
        this.snackbar = { show: true, text: 'Discussão excluída com sucesso!', color: 'success', timeout: 3000 };
      } catch (err) {
        console.error('Erro ao excluir discussão:', err);
        this.snackbar = { show: true, text: 'Erro ao excluir discussão.', color: 'error', timeout: 3000 };
      }
    },

    goToDiscussion(id: number) {
      this.$router.push(`/projects/${this.projectId}/discussions/${id}`);
    },

    confirmClose(discussion: any) {
      this.selectedDiscussion = discussion;
      this.showCloseDialog = true;
    },

    async closeDiscussion() {
      if (!this.selectedDiscussion) return;
      try {
        const res = await this.$axios.post(
          `/v1/projects/${this.projectId}/discussions/${this.selectedDiscussion.id}/close/`
        );
        const index = this.discussions.findIndex(d => d.id === this.selectedDiscussion.id);
        if (index !== -1) {
          this.$set(this.discussions, index, res.data);
        }
        this.showCloseDialog = false;
        this.snackbar = { show: true, text: 'Discussão encerrada com sucesso!', color: 'success', timeout: 3000 };
      } catch (err) {
        console.error('Erro ao encerrar discussão:', err);
        this.snackbar = { show: true, text: 'Erro ao encerrar discussão.', color: 'error', timeout: 3000 };
      }
    },

    confirmReopen(discussion: any) {
      this.selectedDiscussion = discussion;
      const defaultEndDate = new Date();
      defaultEndDate.setDate(defaultEndDate.getDate() + 7);
      this.newEndDate = defaultEndDate.toISOString().substr(0, 10);
      this.showReopenDialog = true;
    },

    async reopenDiscussion() {
      if (!this.selectedDiscussion || !this.newEndDate) return;
      try {
        const res = await this.$axios.post(
          `/v1/projects/${this.projectId}/discussions/${this.selectedDiscussion.id}/reopen/`,
          { end_date: this.newEndDate }
        );
        const index = this.discussions.findIndex(d => d.id === this.selectedDiscussion.id);
        if (index !== -1) {
          this.$set(this.discussions, index, res.data);
        }
        this.showReopenDialog = false;
        this.snackbar = { show: true, text: 'Discussão reaberta com sucesso!', color: 'success', timeout: 3000 };
      } catch (err) {
        console.error('Erro ao reabrir discussão:', err);
        this.snackbar = { show: true, text: 'Erro ao reabrir discussão. Verifique a data e tente novamente.', color: 'error', timeout: 3000 };
      }
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