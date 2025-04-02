<template>
  <v-card>
    <v-card-title>
      <span class="ml-4 headline">Disagreements</span>
    </v-card-title>
    <v-card-text>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="icons.mdiMagnify"
        label="Search"
        single-line
        hide-details
        filled
        style="margin-bottom: 1rem"
      />
      <v-progress-circular
        v-if="isLoading"
        class="ma-3"
        indeterminate
        color="primary"
      />
      <v-alert v-if="error" type="error" dense outlined>
        {{ error }}
      </v-alert>
      <div v-if="!isLoading && disagreements.length === 0">
        <p>No disagreements found.</p>
      </div>
      <div v-if="!isLoading && disagreements.length > 0" class="d-flex justify-center">
        <div style="max-width: 800px; width: 100%;">
          <div
            v-for="group in filteredDisagreements"
            :key="group.signature"
            class="mb-4 d-flex align-center"
          >
            <v-card outlined elevation="2" class="flex-grow-1">
              <v-sheet
                color="primary"
                dark
                class="py-3 px-4 rounded-t-lg d-flex flex-column"
              >
                <div class="text-h6 font-weight-medium">
                  {{ group.snippet }}
                </div>
                <div class="text-body-2">
                  Labels: {{ group.labels.join(', ') }}
                </div>
              </v-sheet>
              <v-card-text>
                <div>
                  Annotation Count: {{ group.count }}
                </div>
              </v-card-text>
              <v-card-actions>
                <v-btn color="secondary" small @click="checkDisagreement(group)">
                  Check Disagreement
                </v-btn>
              </v-card-actions>
            </v-card>
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { mdiMagnify } from '@mdi/js'

interface LabelType {
  id: number;
  text: string;
  background_color: string;
}

interface ExtractedLabels {
  text: string;
  spans: any; // Adjust type if needed
  labelTypes: LabelType[];
}

interface Annotation {
  id: number;
  dataset_item_id: number;
  extracted_labels: ExtractedLabels;
  additional_info: any;
  created_at: string;
  updated_at: string;
  annotator: number;
}

export default Vue.extend({
  name: 'DisagreementsPage',
  data() {
    return {
      disagreements: [] as Array<{
        signature: string;
        snippet: string;
        labels: string[];
        count: number;
        annotations: Annotation[];
      }>,
      search: '',
      isLoading: false,
      error: '',
      icons: {
        mdiMagnify
      }
    }
  },

  layout: 'project',
  
  computed: {
    filteredDisagreements() {
      if (!this.search) return this.disagreements;
      return this.disagreements.filter(group =>
        group.snippet.toLowerCase().includes(this.search.toLowerCase())
      );
    }
  },
  mounted() {
    this.fetchDisagreements();
  },
  methods: {
    async fetchDisagreements() {
      this.isLoading = true;
      const projectId = Number(this.$route.params.id);
      try {
        // Fetch all annotations for the project (adjust query params as needed)
        const response = await axios.get(`/v1/annotations/`, { params: { project: projectId } });
        const annotations: Annotation[] = response.data.results || response.data;

        // Group annotations by common extracted text and labelTypes.
        // We'll compute a signature from the text and a sorted JSON string of labelTypes.
        const groupsMap: { [key: string]: any } = {};

        annotations.forEach(annotation => {
          const extracted = annotation.extracted_labels;
          if (!extracted || !extracted.text || !extracted.labelTypes) return;

          // Sort labelTypes by id to ensure consistent ordering.
          const sortedLabels = [...extracted.labelTypes].sort((a, b) => a.id - b.id);
          const signatureKey = JSON.stringify({
            text: extracted.text,
            labelTypes: sortedLabels.map(label => ({ id: label.id, text: label.text }))
          });

          if (!groupsMap[signatureKey]) {
            groupsMap[signatureKey] = {
              signature: signatureKey,
              snippet: extracted.text.substring(0, 100),
              labels: sortedLabels.map(label => label.text),
              annotations: []
            };
          }
          groupsMap[signatureKey].annotations.push(annotation);
        });
        const groups: any[] = [];
        Object.keys(groupsMap).forEach(signature => {
          const group = groupsMap[signature];
          if (group.annotations.length < 2) return;

          let spansDiffer = false;
          for (let i = 0; i < group.annotations.length; i++) {
            for (let j = i + 1; j < group.annotations.length; j++) {
              const spans1 = group.annotations[i].extracted_labels.spans;
              const spans2 = group.annotations[j].extracted_labels.spans;
              if (JSON.stringify(spans1) !== JSON.stringify(spans2)) {
                spansDiffer = true;
                break;
              }
            }
            if (spansDiffer) break;
          }
          if (spansDiffer) {
            groups.push({
              signature: group.signature,
              snippet: group.snippet,
              labels: group.labels,
              count: group.annotations.length,
              annotations: group.annotations
            });
          }
        });
        this.disagreements = groups;
      } catch (err: any) {
        console.error('Error fetching annotations:', err.response || err.message);
        this.error = 'Failed to load disagreements.';
      } finally {
        this.isLoading = false;
      }
    },
    checkDisagreement(group: any) {
      // Navigate to a detail page for this disagreement group.
      // Ensure a route named "DisagreementDetail" is configured.
      this.$router.push({ name: 'DisagreementDetail', params: { signature: group.signature } });
    }
  }
});
</script>

<style scoped>
.selected-card {
  border: 2px solid #1976D2;
}
</style>