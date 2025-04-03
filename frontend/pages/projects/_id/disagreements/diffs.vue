<template>
  <v-card>
    <v-card-title class="black--text text-center">
      <span class="headline">Differences</span>
      <v-chip-group column>
        <v-chip
          v-for="(label, idx) in allLabels"
          :key="idx"
          :color="label.color"
          :text-color="contrastColor(label.color)"
          small
          class="ma-1 non-clickable"
        >
          {{ label.text }}
        </v-chip>
      </v-chip-group>
    </v-card-title>
    <v-card-text>
      <v-progress-circular
        v-if="isLoading"
        indeterminate
        color="primary"
        class="ma-3"
      />
      <v-alert v-if="error" type="error" dense class="mb-4">
        {{ error }}
      </v-alert>
      <div v-if="!isLoading && annotations.length < 2">
        <p>Not enough annotations to compare.</p>
      </div>
      <div v-if="!isLoading && annotations.length >= 2" class="diff-container">

        <v-card class="diff-card" outlined>
          <v-card-title class="primary white--text text-center">
            Left
          </v-card-title>
          <v-card-text class="diff-canvas">
            <div class="diff-annotation-text" v-if="leftAnnotation"
              v-html="formattedLeftText"></div>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn small @click="prevLeft" :disabled="navigationDisabled ||
            leftIndex === 0">Prev</v-btn>
            <v-btn small @click="nextLeft" :disabled="navigationDisabled ||
            leftIndex === annotations.length - 1">Next</v-btn>
          </v-card-actions>
        </v-card>

        <div class="switch-button">
          <v-btn icon @click="swapAnnotations">
            <v-icon>{{ icons.mdiSwapHorizontal }}</v-icon>
          </v-btn>
        </div>

        <v-card class="diff-card" outlined>
          <v-card-title class="primary white--text text-center">
            Right
          </v-card-title>
          <v-card-text class="diff-canvas">
            <div class="diff-annotation-text" v-if="rightAnnotation"
              v-html="formattedRightText"></div>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn small @click="prevRight" :disabled="navigationDisabled ||
            rightIndex === 0">Prev</v-btn>
            <v-btn small @click="nextRight" :disabled="navigationDisabled ||
            rightIndex === annotations.length - 1">Next</v-btn>
          </v-card-actions>
        </v-card>
      </div>
      <v-checkbox v-model="showDifferences" label="Toggle Differences" class="mt-2"></v-checkbox>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
// @ts-nocheck
import Vue from 'vue'
import axios from 'axios'
import { mdiSwapHorizontal } from '@mdi/js'

interface AnnotationBackend {
  id: number;
  extracted_labels: {
    text: string;
    spans: Array<{ label: number; start_offset: number; end_offset: number }>;
    labelTypes: Array<{
      id: number;
      text: string;
      background_color: string;
      text_color?: string;
      suffixKey?: string;
    }>;
  };
}

interface AnnotationTransformed {
  id: number;
  text: string;
  entities: Array<{
    id: number;
    start: number;
    end: number;
    label: { id: number; text: string; color: string; textColor: string; suffixKey: string };
  }>;
  entityLabels: Array<{ id: number; text: string; color: string;
    textColor: string; suffixKey: string }>;
}

export default Vue.extend({
  name: 'DiffsPage',
  data() {
    return {
      annotations: [] as AnnotationTransformed[],
      leftIndex: 0,
      rightIndex: 1,
      isLoading: false,
      error: '',
      icons: { mdiSwapHorizontal },
      isRTL: false,
      showDifferences: false
    }
  },
  layout: 'project',
  computed: {
    navigationDisabled(): boolean {
      return this.annotations.length === 2;
    },
    leftAnnotation(): AnnotationTransformed | null {
      return this.annotations[this.leftIndex] || null;
    },
    rightAnnotation(): AnnotationTransformed | null {
      return this.annotations[this.rightIndex] || null;
    },
    formattedLeftText(): string {
      return (this.leftAnnotation && this.rightAnnotation) ? this.generateAnnotatedText(this.leftAnnotation, this.rightAnnotation) : "";
    },
    formattedRightText(): string {
      return (this.rightAnnotation && this.leftAnnotation) ? this.generateAnnotatedText(this.rightAnnotation, this.leftAnnotation) : "";
    },
    allLabels(): Array<{ id: number; text: string; color: string }> {
      if (this.leftAnnotation && this.leftAnnotation.entityLabels) {
        const seen = new Set();
        return this.leftAnnotation.entityLabels.filter(label => {
          if (seen.has(label.id)) return false;
          seen.add(label.id);
          return true;
        }).map(label => ({
          id: label.id,
          text: label.text,
          color: label.color
        }));
      }
      return [];
    }
  },
  mounted() {
    this.fetchAnnotations();
  },
  methods: {
    async fetchAnnotations() {
      this.isLoading = true;
      try {
        const response = await axios.get(`/v1/annotations/`, { params: { project: this.$route.params.id } });
        const data: AnnotationBackend[] = response.data.results || response.data;
        const groups: { [signature: string]: AnnotationBackend[] } = {};

        data.forEach(annotation => {
          const extracted = annotation.extracted_labels;
          if (!extracted || !extracted.text || !extracted.labelTypes || !extracted.spans) return;

          const usedLabelIds = new Set(extracted.spans.map((span: any) => span.label));
          const chosenLabels = extracted.labelTypes.filter(label => usedLabelIds.has(label.id));
          const sortedLabels = [...chosenLabels].sort((a, b) => a.id - b.id);

          const signatureKey = JSON.stringify({
            text: extracted.text,
            labelTypes: sortedLabels.map(label => ({ id: label.id, text: label.text }))
          });
          
          if (!groups[signatureKey]) { groups[signatureKey] = []; }
          groups[signatureKey].push(annotation);
        });

        const leftQuery = this.$route.query.left;
        const rightQuery = this.$route.query.right;
        const selectedGroup = Object.values(groups).find(group =>
          group.some(ann => String(ann.id) === leftQuery) &&
          group.some(ann => String(ann.id) === rightQuery)
        );

        if (selectedGroup && selectedGroup.length >= 2) {
          this.annotations = selectedGroup.map(ann => {
            const extracted = ann.extracted_labels;
            const usedLabelIds = new Set(extracted.spans.map((span: any) => span.label));
            const chosenLabels = extracted.labelTypes.filter(label => usedLabelIds.has(label.id));
            const sortedLabels = [...chosenLabels].sort((a, b) => a.id - b.id);
            const labels = sortedLabels.map(label => ({
              id: label.id,
              text: label.text,
              color: label.background_color,
              textColor: label.text_color || '#ffffff',
              suffixKey: label.suffixKey ? label.suffixKey : label.text
            }));
            return {
              id: ann.id,
              text: extracted.text,
              entities: extracted.spans.map((span, i) => ({
                id: i,
                start: span.start_offset,
                end: span.end_offset,
                label: labels.find(l => l.id === span.label) || { id: span.label, text: '', color: '#000000', textColor: '#ffffff', suffixKey: '' }
              })),
              entityLabels: labels
            };
          });
          this.leftIndex = 0;
          this.rightIndex = 1;
        } else {
          this.error = 'No matching disagreement group found.';
          this.annotations = [];
        }
      } catch (err: any) {
        console.error(err);
        this.error = "Error: Can't access our database!";
      } finally {
        this.isLoading = false;
      }
    },
    generateAnnotatedText(annotation: AnnotationTransformed, other: AnnotationTransformed): string {
      const escapeHTML = (str: string) =>
        str.replace(/&/g, "&amp;")
           .replace(/</g, "&lt;")
           .replace(/>/g, "&gt;");
      const text = annotation.text;

      // Gather all unique boundaries (start and end positions) from both annotations
      const boundaries = new Set<number>();
      annotation.entities.forEach(span => {
        boundaries.add(span.start);
        boundaries.add(span.end);
      });
      other.entities.forEach(span => {
        boundaries.add(span.start);
        boundaries.add(span.end);
      });

      const sortedBoundaries = Array.from(boundaries).sort((a, b) => a - b);
      let html = "";

      for (let i = 0; i < sortedBoundaries.length - 1; i++) {
        const start = sortedBoundaries[i];
        const end = sortedBoundaries[i + 1];
        const segment = text.substring(start, end);

        const currentSpan = annotation.entities.find(s => s.start <= start && s.end >= end);
        const otherSpan = other.entities.find(s => s.start <= start && s.end >= end);

        let style = "";
        if (currentSpan) {
          style = `border-bottom: 3px solid ${currentSpan.label.color};`;
        }
        if (this.showDifferences && otherSpan) {
          if (!currentSpan || (currentSpan && currentSpan.label.id !== otherSpan.label.id)) {
            style = 'border-bottom: 3px dashed #FF5252;';
          }
        }

        html += `<span style="${style}" title="${currentSpan ? currentSpan.label.text : (otherSpan ? otherSpan.label.text : '')}">${escapeHTML(segment)}</span>`;
      }

      const firstBoundary = sortedBoundaries[0] || 0;
      const prefix = text.substring(0, firstBoundary);
      const lastBoundary = sortedBoundaries[sortedBoundaries.length - 1] || text.length;
      const suffix = text.substring(lastBoundary);

      html = (prefix ? escapeHTML(prefix) : "") + html + (suffix ? escapeHTML(suffix) : "");
      return html;
    },
    swapAnnotations() {
      const temp = this.leftIndex;
      this.leftIndex = this.rightIndex;
      this.rightIndex = temp;
    },
    prevLeft() {
      if (this.leftIndex > 0) {
        this.leftIndex--;
        if (this.leftIndex === this.rightIndex) {
          this.leftIndex > 0 ? this.leftIndex-- : this.leftIndex++;
        }
      }
    },
    nextLeft() {
      if (this.leftIndex < this.annotations.length - 1) {
        this.leftIndex++;
        if (this.leftIndex === this.rightIndex) {
          this.leftIndex < this.annotations.length - 1 ? this.leftIndex++ : this.leftIndex--;
        }
      }
    },
    prevRight() {
      if (this.rightIndex > 0) {
        this.rightIndex--;
        if (this.rightIndex === this.leftIndex) {
          this.rightIndex > 0 ? this.rightIndex-- : this.rightIndex++;
        }
      }
    },
    nextRight() {
      if (this.rightIndex < this.annotations.length - 1) {
        this.rightIndex++;
        if (this.rightIndex === this.leftIndex) {
          this.rightIndex < this.annotations.length - 1 ? this.rightIndex++ : this.rightIndex--;
        }
      }
    },
    checkDisagreement() {
      const projectId = this.$route.params.id;
      const leftId = this.leftAnnotation ? String(this.leftAnnotation.id) : '';
      const rightId = this.rightAnnotation ? String(this.rightAnnotation.id) : '';
      this.$router.push({
        path: `/projects/${projectId}/disagreements/diffs`,
        query: { left: leftId, right: rightId }
      });
    },
    contrastColor(color: string): string {
      const r = parseInt(color.slice(1, 3), 16);
      const g = parseInt(color.slice(3, 5), 16);
      const b = parseInt(color.slice(5, 7), 16);
      const brightness = (r * 299 + g * 587 + b * 114) / 1000;
      return brightness > 125 ? 'black' : 'white';
    }
  }
});
</script>

<style scoped>
.diff-container {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  overflow-x: auto;
  gap: 16px;
  padding: 8px;
}
.diff-card {
  flex: 0 0 auto;
  width: 45%;
}
.switch-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 5%;
}
.diff-canvas {
  height: 250px;
  overflow-y: auto;
  padding: 8px;
}
.diff-annotation-text {
  font-size: 1rem !important;
  font-weight: 500;
  line-height: 1.5rem;
  font-family: 'Roboto', sans-serif !important;
  color: black;
  white-space: pre-wrap; /* Preserve spaces and line breaks */
  word-wrap: break-word; /* Break long words if necessary */
}
.label-legend {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 8px;
}
.legend-item {
  display: inline-flex;
  align-items: center;
  margin: 0 8px;
}
.legend-ball {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 4px;
}
.legend-text {
  font-size: 0.8rem;
}
.non-clickable {
  pointer-events: none;
}
</style>