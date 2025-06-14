<template>
  <v-container fluid>
    <v-alert
      v-if="databaseError"
      type="error"
      dense
      class="mb-4"
    >
      Database unavailable. Please try again later.
    </v-alert>

    <v-row>
      <v-col cols="12">
        <v-card class="elevation-4">
          <v-card-title class="headline primary white--text">
            Discrepancy Analysis
            <v-spacer></v-spacer>
            <v-chip color="white" text-color="primary" class="ml-2">
              Threshold: {{ project.minPercentage }}%
            </v-chip>
          </v-card-title>

          <v-card-text class="pt-4">
            <discrepancy-list
              v-model="selected"
              :items="items"
              :is-loading="isLoading"
              :discrepancy-threshold="project.minPercentage"
            />
          </v-card-text>

          <v-card-actions v-if="hasDiscrepancies" class="justify-center">
            <v-btn
              color="primary"
              class="text-center"
              @click="goToChat"
            >
              <v-icon left>mdi-message-text</v-icon>
              Discuss Discrepancies
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import DiscrepancyList from '~/components/discrepancy/DiscrepancyList.vue'
import type { Percentage } from '~/domain/models/metrics/metrics'

export default Vue.extend({
  name: 'ProjectExamplesDiscrepancy',
  components: { DiscrepancyList },

  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      items: {} as Percentage,
      isLoading: false,
      selected: {} as Percentage,
      databaseError: false,
      checkInterval: null as NodeJS.Timeout | null
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      if (this.project.canDefineCategory) {
        this.items = await this.$repositories.metrics.fetchCategoryPercentage(this.projectId)
      }
      if (this.project.canDefineSpan) {
        this.items = await this.$repositories.metrics.fetchSpanPercentage(this.projectId)
      }
      if (this.project.canDefineRelation) {
        this.items = await this.$repositories.metrics.fetchRelationPercentage(this.projectId)
      }
      this.databaseError = false
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
      this.databaseError = true
    } finally {
      this.isLoading = false
    }
  },

  mounted() {
    // Inicia a verificação periódica
    this.checkDatabaseConnection()
    this.checkInterval = setInterval(this.checkDatabaseConnection, 1000)
  },

  beforeDestroy() {
    // Limpa o intervalo quando o componente é destruído
    if (this.checkInterval) {
      clearInterval(this.checkInterval)
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    projectId(): string {
      return this.$route.params.id
    },
    hasDiscrepancies(): boolean {
      return Object.values(this.items).some(item => 
        Object.values(item).some(percentage => percentage < this.project.minPercentage)
      )
    }
  },

  watch: {
    project: {
      handler(newVal) {
        if (newVal && (
          newVal.canDefineCategory ||
          newVal.canDefineSpan ||
          newVal.canDefineRelation
        )) {
          this.$fetch()
        }
      },
      immediate: true,
      deep: true
    }
  },

  methods: {
    goToChat() {
      this.$router.push(
        `/projects/${this.projectId}/examples/19/discrepancies/detail`
      )
    },
    async checkDatabaseConnection() {
      try {
        // Tenta buscar uma pequena quantidade de dados para verificar a conexão
        await this.$repositories.metrics.fetchCategoryPercentage(this.projectId)
        this.databaseError = false
      } catch (error) {
        console.error('Erro na verificação da conexão:', error)
        this.databaseError = true
      }
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>