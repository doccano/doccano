<template>
  <v-card>
    <v-card-title class="pb-0">
      <h1 class="text-h4">Versions Report</h1>
      <v-spacer />
      <div class="d-flex justify-end mb-4">
        <v-btn
          :loading="isExporting"
          color="primary"
          @click="exportToCsv"
          class="mr-2"
        >
          <v-icon left>
            {{ mdiDownload }}
          </v-icon>
          Export CSV
        </v-btn>
        <v-btn
          :loading="isExportingPdf"
          color="secondary"
          @click="exportToPdf"
        >
          <v-icon left>
            {{ mdiFilePdfBox }}
          </v-icon>
          Export PDF
        </v-btn>
      </div>
    </v-card-title>

    <!-- Filtros -->
    <v-card-text>
      <v-row>
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.version"
            :items="versionOptions"
            label="Filter by Version"
            clearable
            outlined
            dense
            @change="loadReport"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.status"
            :items="statusOptions"
            label="Filter by Status"
            clearable
            outlined
            dense
            @change="loadReport"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.user"
            :items="userOptions"
            label="Filter by User"
            clearable
            outlined
            dense
            @change="loadReport"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-btn
            color="secondary"
            outlined
            @click="clearFilters"
          >
            <v-icon left>{{ mdiFilterRemove }}</v-icon>
            Clear Filters
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>

    <!-- Loading -->
    <div v-if="loading" class="text-center pa-4">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      />
      <div class="mt-2">Loading report...</div>
    </div>

    <!-- Relatório por versão -->
    <div v-else>
      <div v-for="version in reportData.versions" :key="version.version" class="mb-6">
        <!-- Header da versão -->
        <v-card-subtitle class="text-h5 pa-4 bg-grey lighten-4">
          <v-row align="center">
            <v-col>
              <v-chip
                :color="version.version === reportData.current_version ? 'primary' : 'grey'"
                label
                small
                class="mr-2"
              >
                Version {{ version.version }}
              </v-chip>
              <span class="text-subtitle-1">
                Created {{ formatDate(version.created_at) }}
                <span v-if="version.created_by">by {{ version.created_by }}</span>
              </span>
            </v-col>
            <v-col cols="auto">
              <v-chip
                color="info"
                outlined
                small
                class="mr-2"
              >
                {{ version.total_examples }} examples
              </v-chip>
              <v-chip
                v-if="version.discrepant_examples > 0"
                color="error"
                outlined
                small
                class="mr-2"
              >
                {{ version.discrepant_examples }} discrepant
              </v-chip>
              <v-chip
                v-if="version.non_discrepant_examples > 0"
                color="success"
                outlined
                small
              >
                {{ version.non_discrepant_examples }} non-discrepant
              </v-chip>
            </v-col>
          </v-row>
        </v-card-subtitle>

        <!-- Tabela de exemplos -->
        <v-data-table
          :headers="headers"
          :items="version.examples"
          :items-per-page="10"
          class="elevation-1"
          :loading="loading"
        >
          <!-- Status chip -->
          <template #[`item.status`]="{ item }">
            <v-chip
              :color="item.status === 'Finished' ? 'success' : 'warning'"
              small
              text-color="white"
            >
              {{ item.status }}
            </v-chip>
          </template>

          <!-- Discrepancy indicator -->
          <template #[`item.has_discrepancy`]="{ item }">
            <v-chip
              :color="item.has_discrepancy ? 'error' : 'success'"
              small
              text-color="white"
            >
              {{ item.has_discrepancy ? 'Discrepant' : 'Non Discrepant' }}
            </v-chip>
          </template>

          <!-- Text preview -->
          <template #[`item.example_text`]="{ item }">
            <span class="text-truncate" style="max-width: 300px; display: block;">
              {{ item.example_text }}
            </span>
          </template>

          <!-- Label percentages -->
          <template #[`item.label_percentages`]="{ item }">
            <div class="d-flex flex-wrap gap-1">
              <v-chip
                v-for="(data, label) in item.label_percentages"
                :key="label"
                small
                outlined
                class="ma-1"
              >
                {{ label }} ({{ data.percentage }}%)
              </v-chip>
            </div>
          </template>

          <!-- Assigned users -->
          <template #[`item.assigned_users`]="{ item }">
            <div class="d-flex flex-wrap gap-1">
              <v-chip
                v-for="user in item.assigned_users"
                :key="user"
                small
                color="blue"
                text-color="white"
                class="ma-1"
              >
                {{ user }}
              </v-chip>
            </div>
          </template>

          <!-- Confirmed users -->
          <template #[`item.confirmed_users`]="{ item }">
            <div class="d-flex flex-wrap gap-1">
              <v-chip
                v-for="user in item.confirmed_users"
                :key="user"
                small
                color="green"
                text-color="white"
                class="ma-1"
              >
                {{ user }}
              </v-chip>
            </div>
          </template>
        </v-data-table>
      </div>

      <!-- Empty state -->
      <div v-if="reportData.versions.length === 0" class="text-center pa-8">
        <v-icon size="64" color="grey">{{ mdiFileDocumentOutline }}</v-icon>
        <div class="text-h6 mt-2 grey--text">No versions found</div>
        <div class="text-body-2 grey--text">Try adjusting your filters or create some versions first.</div>
      </div>
    </div>
  </v-card>
</template>

<script>
import {
  mdiDownload,
  mdiFilterRemove,
  mdiFileDocumentOutline,
  mdiFilePdfBox
} from '@mdi/js'

export default {
  name: 'VersionsReport',
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      loading: false,
      isExporting: false,
      isExportingPdf: false,
      reportData: {
        project_id: null,
        project_name: '',
        current_version: 1,
        threshold: 0,
        versions: []
      },
      filters: {
        version: null,
        status: null,
        user: null
      },
      headers: [
        {
          text: 'Example ID',
          value: 'example_id',
          width: 100
        },
        {
          text: 'Text',
          value: 'example_text',
          width: 300,
          sortable: false
        },
        {
          text: 'Status',
          value: 'status',
          width: 120
        },
        {
          text: 'Discrepancy',
          value: 'has_discrepancy',
          width: 130
        },
        {
          text: 'Label Percentages',
          value: 'label_percentages',
          width: 250,
          sortable: false
        },
        {
          text: 'Assigned Users',
          value: 'assigned_users',
          width: 150,
          sortable: false
        },
        {
          text: 'Confirmed Users',
          value: 'confirmed_users',
          width: 150,
          sortable: false
        },
        {
          text: 'Total Annotations',
          value: 'total_annotations',
          width: 120
        }
      ],
      mdiDownload,
      mdiFilterRemove,
      mdiFileDocumentOutline,
      mdiFilePdfBox
    }
  },

  computed: {
    projectId() {
      return this.$route.params.id
    },

    versionOptions() {
      const versions = this.reportData.versions.map(v => ({
        text: `Version ${v.version}`,
        value: v.version
      }))
      return versions
    },

    statusOptions() {
      return [
        { text: 'Discrepant', value: 'discrepant' },
        { text: 'Non Discrepant', value: 'non_discrepant' }
      ]
    },

    userOptions() {
      // Extrair todos os usuários únicos dos dados
      const users = new Set()
      this.reportData.versions.forEach(version => {
        version.examples.forEach(example => {
          example.assigned_users.forEach(user => users.add(user))
        })
      })
      
      return Array.from(users).map(user => ({
        text: user,
        value: user
      }))
    }
  },

  async mounted() {
    await this.loadReport()
  },

  methods: {
    async loadReport() {
      try {
        this.loading = true
        this.reportData = await this.$repositories.project.getVersionsReport(this.projectId, this.filters)
      } catch (error) {
        console.error('Error loading versions report:', error)
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Error loading versions report'
        })
      } finally {
        this.loading = false
      }
    },

    exportToCsv() {
      this.isExporting = true
      this.$repositories.project.exportVersionsReport(this.projectId, this.filters)
        .then(() => {
          this.$store.dispatch('notification/setNotification', {
            color: 'success',
            text: 'Report exported successfully'
          })
        })
        .catch((error) => {
          console.error('Error exporting report:', error)
          this.$store.dispatch('notification/setNotification', {
            color: 'error',
            text: 'Error exporting report'
          })
        })
        .finally(() => {
          this.isExporting = false
        })
    },

    exportToPdf() {
      this.isExportingPdf = true
      this.$repositories.project.exportVersionsReportPdf(this.projectId, this.filters)
        .then(() => {
          this.$store.dispatch('notification/setNotification', {
            color: 'success',
            text: 'Report exported successfully'
          })
        })
        .catch((error) => {
          console.error('Error exporting report:', error)
          this.$store.dispatch('notification/setNotification', {
            color: 'error',
            text: 'Error exporting report'
          })
        })
        .finally(() => {
          this.isExportingPdf = false
        })
    },

    clearFilters() {
      this.filters = {
        version: null,
        status: null,
        user: null
      }
      this.loadReport()
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('pt-PT', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.gap-1 > * {
  margin: 2px;
}
</style> 