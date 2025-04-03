<template>
  <v-card>
    <v-card-title>
      <v-btn
        class="text-capitalize ms-2"
        outlined
        @click="clearDisagreements"
      >
        Clear
      </v-btn>
    </v-card-title>
    <v-card-text>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="icons.mdiMagnify"
        label="Search"
        single-line
        hide-details
        filled
        class="mb-4"
      />
      <v-progress-circular
        v-if="isLoading"
        class="ma-3"
        indeterminate
        color="primary"
      />
      <v-alert v-if="error" type="error" dense class="mb-4">
        {{ error }}
      </v-alert>
      <div v-if="!isLoading && disagreements.length === 0">
        <p>No disagreements found.</p>
      </div>
      <div v-if="!isLoading && disagreements.length > 0" class="horizontal-scroll-container">
        <div
          v-for="disagreement in filteredDisagreements"
          :key="disagreement.signature"
          class="disagreement-block"
        >
          <v-card outlined class="pa-3">
            <v-sheet color="primary" dark class="pa-2 mb-2 rounded-t-lg">
              <div class="text-h6 font-weight-medium">
                {{ disagreement.snippet }}
              </div>
            </v-sheet>

            <div class="d-flex flex-wrap mb-2">
              <v-chip
                v-for="(label, idx) in disagreement.labels"
                :key="idx"
                :color="label.backgroundColor"
                :text-color="contrastColor(label.backgroundColor)"
                small
                class="ma-1"
              >
                {{ label.text }}
              </v-chip>
            </div>

            <div class="mb-2 text-center">
              <strong>Annotations in conflict:</strong> {{ disagreement.count }}
            </div>
            <v-card-actions class="justify-center">
              <v-btn color="secondary" small @click="checkDisagreement(disagreement)">
                Check Disagreement
              </v-btn>
            </v-card-actions>
          </v-card>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
// @ts-nocheck
import Vue from 'vue'
import axios from 'axios'
import { mdiMagnify, mdiAlertCircle } from '@mdi/js'

interface LabelType {
  id: number;
  text: string;
  background_color: string;
}

interface ExtractedLabels {
  text: string;
  spans: any;
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
        labels: Array<{ text: string; backgroundColor: string }>;
        count: number;
        annotations: Annotation[];
      }>,
      search: '',
      isLoading: false,
      error: '',
      icons: {
        mdiMagnify,
        mdiAlertCircle
      }
    }
  },

  layout: 'project',

  computed: {
    filteredDisagreements() {
      const disagreements = (this as any).disagreements;
      if (!this.search) return disagreements;
      return disagreements.filter((disagreement: any) =>
        disagreement.snippet.toLowerCase().includes(this.search.toLowerCase())
      );
    },
    canDelete(): boolean {
      return false;
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
        const response = await axios.get(`/v1/annotations/`, { params: { project: projectId } });
        const annotations: Annotation[] = response.data.results || response.data;

        const disagreementsMap: { [key: string]: any } = {};

        annotations.forEach(annotation => {
          const extracted = annotation.extracted_labels;
          if (!extracted || !extracted.text || !extracted.labelTypes || !extracted.spans) return;

          const usedLabelIds = extracted.spans.map((span: any) => span.label);
          
          const usedLabels = extracted.labelTypes.filter(label => usedLabelIds.includes(label.id));
          
          const dedupedUsedLabels = Array.from(new Set(
            usedLabels.map(label => JSON.stringify({
              id: label.id,
              text: label.text,
              background_color: label.background_color
            }))
          )).map(str => JSON.parse(str));
          
          const sortedLabels = dedupedUsedLabels.sort((a, b) => a.id - b.id);
          
          const signatureKey = JSON.stringify({
            text: extracted.text,
            labelTypes: sortedLabels.map(label => ({ id: label.id, text: label.text }))
          });
          
          if (!disagreementsMap[signatureKey]) {
            disagreementsMap[signatureKey] = {
              signature: signatureKey,
              snippet: extracted.text.substring(0, 100),
              labels: sortedLabels.map(label => ({
                text: label.text,
                backgroundColor: label.background_color
              })),
              annotations: []
            };
          }
          disagreementsMap[signatureKey].annotations.push(annotation);
        });

        const disagreements: any[] = [];
        Object.keys(disagreementsMap).forEach(signature => {
          const disagreement = disagreementsMap[signature];
          if (disagreement.annotations.length < 2) return;

          let spansDiffer = false;
          for (let i = 0; i < disagreement.annotations.length; i++) {
            for (let j = i + 1; j < disagreement.annotations.length; j++) {
              const spans1 = disagreement.annotations[i].extracted_labels.spans;
              const spans2 = disagreement.annotations[j].extracted_labels.spans;
              if (JSON.stringify(spans1) !== JSON.stringify(spans2)) {
                spansDiffer = true;
                break;
              }
            }
            if (spansDiffer) break;
          }
          if (spansDiffer) {
            disagreements.push({
              signature: disagreement.signature,
              snippet: disagreement.snippet,
              labels: disagreement.labels,
              count: disagreement.annotations.length,
              annotations: disagreement.annotations
            });
          }
        });
        this.disagreements = disagreements;
      } catch (err: any) {
        console.error('Error fetching annotations:', err.response || err.message);
        this.error = "Error: Can't access our database!";
      } finally {
        this.isLoading = false;
      }
    },
    clearDisagreements() {
      this.disagreements = [];
    },
    checkDisagreement(disagreement: any) {
      const projectId = this.$route.params.id;
      const leftId = disagreement.annotations[0] ? disagreement.annotations[0].id : null;
      const rightId = disagreement.annotations[1] ? disagreement.annotations[1].id : null;
      this.$router.push({
        path: `/projects/${projectId}/disagreements/diffs`,
        query: { left: leftId, right: rightId }
      });
    },
    goToAdd() {
      this.$router.push({ name: 'AddDisagreement' });
    },

    contrastColor(hexColor: string): string {
      if (!hexColor) return '#000000';
      const color = hexColor.replace('#', '');
      let r, g, b;
      if (color.length === 3) {
        r = parseInt(color[0] + color[0], 16);
        g = parseInt(color[1] + color[1], 16);
        b = parseInt(color[2] + color[2], 16);
      } else {
        r = parseInt(color.substring(0, 2), 16);
        g = parseInt(color.substring(2, 4), 16);
        b = parseInt(color.substring(4, 6), 16);
      }
      const brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
      return brightness < 0.5 ? '#FFFFFF' : '#000000';
    }
  }
});
</script>

<style scoped>
.horizontal-scroll-container {
  display: flex;
  flex-direction: row;
  overflow-x: auto;
  padding: 8px;
}
.disagreement-block {
  flex: 0 0 auto;
  width: 300px;
  margin-right: 16px;
}
</style>