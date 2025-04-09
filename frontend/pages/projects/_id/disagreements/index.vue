<template>
  <v-card>
    <v-card-title>
      Disagreements
    </v-card-title>
    <v-card-text>
      <v-progress-circular v-if="isLoading" indeterminate color="primary" />
      <v-alert v-if="error" type="error" dense outlined>
        {{ error }}
      </v-alert>
      <div v-if="!isLoading && disagreements.length === 0">
        <p>No disagreements found.</p>
      </div>
      <v-list v-else>
        <v-list-item v-for="disagreement in disagreements" :key="disagreement.id">
          <v-list-item-content>
            <v-list-item-title>
              Disagreement on Dataset Item {{ disagreement.dataset_item_id }}
            </v-list-item-title>
            <v-list-item-subtitle>
              Status: {{ disagreement.status }}
            </v-list-item-subtitle>
            <v-list-item-subtitle v-if="disagreement.disagreement_details">
              Details: {{ disagreement.disagreement_details | json }}
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn icon @click="resolveDisagreement(disagreement)">
              <v-icon>mdi-check</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { APIDisagreementRepository } from '@/repositories/disagreement/apiDisagreementRepository'
export default Vue.extend({
  name: 'DisagreementsPage',
  data() {
    return {
      disagreements: [] as any[],
      isLoading: false,
      error: ''
    }
  },
  mounted() {
    this.fetchDisagreements()
  },
  methods: {
    async fetchDisagreements() {
      this.isLoading = true
      const projectId = Number(this.$route.params.id)
      try {
        const repo = new APIDisagreementRepository()
        this.disagreements = await repo.list(projectId)
      } catch (err: any) {
        console.error('Error fetching disagreements:', err.response || err.message)
        this.error = "Failed to load disagreements."
      } finally {
        this.isLoading = false
      }
    },
    resolveDisagreement(disagreement: any) {
      const projectId = Number(this.$route.params.id)
      this.$router.push({
        path: this.localePath(`/projects/${projectId}/disagreements/${disagreement.id}/resolve`)
      })
    }
  },
  filters: {
    json(value: any) {
      return JSON.stringify(value, null, 2)
    }
  }
})
</script>

<style scoped>
</style>