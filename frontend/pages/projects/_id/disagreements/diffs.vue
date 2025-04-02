<template>
    <v-card>
      <v-card-title>
        <span class="headline">Diff Checker</span>
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
          <!-- Left Canvas -->
          <v-card class="diff-card" outlined>
            <v-card-title class="primary white--text">
              Left Annotation
            </v-card-title>
            <v-card-text>
              <div class="annotation-text">
                {{ leftAnnotation.text }}
              </div>
              <!-- Optionally, render highlighted spans here -->
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn small @click="prevLeft" :disabled="leftIndex === 0">Prev</v-btn>
              <v-btn small @click="nextLeft" :disabled="leftIndex ===
              annotations.length - 1">Next</v-btn>
            </v-card-actions>
          </v-card>
  
          <!-- Switch Button -->
          <div class="switch-button">
            <v-btn icon @click="swapAnnotations">
              <v-icon>{{ icons.mdiSwapHorizontal }}</v-icon>
            </v-btn>
          </div>
  
          <!-- Right Canvas -->
          <v-card class="diff-card" outlined>
            <v-card-title class="primary white--text">
              Right Annotation
            </v-card-title>
            <v-card-text>
              <div class="annotation-text">
                {{ rightAnnotation.text }}
              </div>
              <!-- Optionally, render highlighted spans here -->
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
  import Vue from 'vue'
  import axios from 'axios'
  import { mdiSwapHorizontal } from '@mdi/js'
  
  interface Annotation {
    id: number;
    text: string;
    spans: any; // Optionally, define a more specific type for spans
    // Other fields as needed...
  }
  
  export default Vue.extend({
    name: 'DiffsPage',
    data() {
      return {
        annotations: [] as Annotation[],
        leftIndex: 0,
        rightIndex: 1,
        isLoading: false,
        error: '',
        icons: {
          mdiSwapHorizontal
        }
      }
    },
    computed: {
      leftAnnotation(): Annotation | null {
        return this.annotations[this.leftIndex] || null;
      },
      rightAnnotation(): Annotation | null {
        return this.annotations[this.rightIndex] || null;
      }
    },
    mounted() {
      this.fetchAnnotations();
    },
    methods: {
      async fetchAnnotations() {
        this.isLoading = true;
        try {
          // Adjust the endpoint as needed.
          const response = await axios.get(`/v1/annotations/diff`, { params: { project: this.$route.params.id } });
          const data = response.data.results || response.data;
          this.annotations = data;
          if (this.annotations.length < 2) {
            this.error = 'Not enough annotations to compare.';
          } else if (this.leftIndex === this.rightIndex) {
            // Ensure the two indices are distinct.
            this.rightIndex = 1;
          }
        } catch (err: any) {
          console.error(err);
          this.error = 'Failed to load annotations for diff.';
        } finally {
          this.isLoading = false;
        }
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
            // Ensure the indices remain distinct
            if (this.leftIndex > 0) this.leftIndex--;
            else this.leftIndex++;
          }
        }
      },
      nextLeft() {
        if (this.leftIndex < this.annotations.length - 1) {
          this.leftIndex++;
          if (this.leftIndex === this.rightIndex) {
            if (this.leftIndex < this.annotations.length - 1) this.leftIndex++;
            else this.leftIndex--;
          }
        }
      },
      prevRight() {
        if (this.rightIndex > 0) {
          this.rightIndex--;
          if (this.rightIndex === this.leftIndex) {
            if (this.rightIndex > 0) this.rightIndex--;
            else this.rightIndex++;
          }
        }
      },
      nextRight() {
        if (this.rightIndex < this.annotations.length - 1) {
          this.rightIndex++;
          if (this.rightIndex === this.leftIndex) {
            if (this.rightIndex < this.annotations.length - 1) this.rightIndex++;
            else this.rightIndex--;
          }
        }
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
  .annotation-text {
    font-size: 1.1rem;
    line-height: 1.5;
    padding: 8px;
  }
  </style>
  