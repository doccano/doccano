<template>
  <v-card>
    <v-card-title class="black--text text-center">
      <span class="headline">Diff Checker</span>
      <div class="label-legend">
        <div v-for="label in allLabels" :key="label.id" class="legend-item">
          <span class="legend-ball" :style="{ backgroundColor: label.color }"></span>
          <span class="legend-text">{{ label.text }}</span>
        </div>
      </div>
    </v-card-title>
    <v-card-text>
      <v-progress-circular
        v-if="isLoading"
        indeterminate
        color="primary"
        class="ma-3"
      />
      <v-alert v-if="error" type="error" dense outlined class="mb-4">
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
            <v-btn small @click="prevLeft" :disabled="leftIndex === 0">Prev</v-btn>
            <v-btn small @click="nextLeft" :disabled="leftIndex
            === annotations.length - 1">Next</v-btn>
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
            <v-btn small @click="prevRight" :disabled="rightIndex === 0">Prev</v-btn>
            <v-btn small @click="nextRight" :disabled="rightIndex
            === annotations.length - 1">Next</v-btn>
          </v-card-actions>
        </v-card>
      </div>
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
  entityLabels: Array<{ id: number; text: string; color:
    string; textColor: string; suffixKey: string }>;
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
      isRTL: false
    }
  },
  layout: 'project',
  computed: {
    leftAnnotation(): AnnotationTransformed | null {
      return this.annotations[this.leftIndex] || null;
    },
    rightAnnotation(): AnnotationTransformed | null {
      return this.annotations[this.rightIndex] || null;
    },
    formattedLeftText(): string {
      return this.leftAnnotation ? this.generateAnnotatedText(this.leftAnnotation) : "";
    },
    formattedRightText(): string {
      return this.rightAnnotation ? this.generateAnnotatedText(this.rightAnnotation) : "";
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
        this.annotations = data.map(ann => {
          const labels = ann.extracted_labels.labelTypes.map(label => ({
            id: label.id,
            text: label.text,
            color: label.background_color,
            textColor: label.text_color || '#ffffff',
            suffixKey: label.suffixKey ? label.suffixKey : label.text
          }));
          return {
            id: ann.id,
            text: ann.extracted_labels.text,
            entities: ann.extracted_labels.spans.map((span, i) => ({
              id: i,
              start: span.start_offset,
              end: span.end_offset,
              label: labels.find(l => l.id === span.label) || { id: span.label, text: '', color: '#000000', textColor: '#ffffff', suffixKey: '' }
            })),
            entityLabels: labels
          }
        });
        if (this.annotations.length < 2) {
          this.error = 'Not enough annotations to compare.';
        } else if (this.leftIndex === this.rightIndex) {
          this.rightIndex = 1;
        }
      } catch (err: any) {
        console.error(err);
        this.error = 'Failed to load annotations for diff.';
      } finally {
        this.isLoading = false;
      }
    },
    generateAnnotatedText(annotation: AnnotationTransformed): string {
      const spans = annotation.entities.slice().sort((a, b) => a.start - b.start);
      const text = annotation.text;
      let html = "";
      let lastIndex = 0;
      const escapeHTML = (str: string) =>
        str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

      spans.forEach(span => {
        html += escapeHTML(text.substring(lastIndex, span.start));
        const spanText = escapeHTML(text.substring(span.start, span.end));
        const color = span.label.color;
        const labelText = span.label.text;
        html += `<span style="border-bottom: 3px solid ${color};" title="${labelText}">${spanText}</span>`;
        lastIndex = span.end;
      });
      html += escapeHTML(text.substring(lastIndex));
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
</style>