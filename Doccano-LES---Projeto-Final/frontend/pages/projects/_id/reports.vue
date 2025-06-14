<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Reports</h1>
      </v-col>
    </v-row>

    <v-row>
      <!-- Annotation Reports Card -->
      <v-col cols="12" md="4">
        <v-card class="h-100">
          <v-card-title>
            <v-icon left color="primary" class="mr-2">{{ mdiLabel }}</v-icon>
            Annotation Reports
          </v-card-title>
          <v-card-text>
            Generate reports about:
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Annotation Statistics</v-list-item-title>
                  <v-list-item-subtitle>Overview of annotation progress and distribution</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Label Distribution</v-list-item-title>
                  <v-list-item-subtitle>Distribution of labels across the dataset</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="generateAnnotationReport">
              Generate Report
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Annotation History Card -->
      <v-col cols="12" md="4">
        <v-card class="h-100">
          <v-card-title>
            <v-icon left color="primary" class="mr-2">{{ mdiHistory }}</v-icon>
            Annotation History
          </v-card-title>
          <v-card-text>
            Generate reports about:
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Annotation Timeline</v-list-item-title>
                  <v-list-item-subtitle>Historical view of annotation activities</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Revision History</v-list-item-title>
                  <v-list-item-subtitle>Track changes and modifications</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="generateHistoryReport">
              Generate Report
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Annotator Reports Card -->
      <v-col cols="12" md="4">
        <v-card class="h-100">
          <v-card-title>
            <v-icon left color="primary" class="mr-2">{{ mdiAccountGroup }}</v-icon>
            Annotator Reports
          </v-card-title>
          <v-card-text>
            Generate reports about:
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Annotator Performance</v-list-item-title>
                  <v-list-item-subtitle>Individual annotator statistics and progress</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Team Performance</v-list-item-title>
                  <v-list-item-subtitle>Overall team statistics and collaboration</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" :to="`/projects/${projectId}/annotator-report`">
              Generate Report
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {
  mdiLabel,
  mdiHistory,
  mdiAccountGroup
} from '@mdi/js'

export default {
  layout: 'project',
  data() {
    return {
      mdiLabel,
      mdiHistory,
      mdiAccountGroup
    }
  },
  computed: {
    projectId() {
      return this.$route.params.id
    }
  },
  methods: {
    generateAnnotationReport() {
      this.$router.push(`/projects/${this.projectId}/disagreements-report`)
    },
    generateHistoryReport() {
      // TODO: Implement history report generation
      console.log('Generating history report...')
    }
  }
}
</script>

<style scoped>
.h-100 {
  height: 100%;
}
</style> 