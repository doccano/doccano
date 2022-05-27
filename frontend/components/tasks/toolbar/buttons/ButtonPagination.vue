<template>
  <div class="v-data-footer">
    <v-edit-dialog large persistent @save="changePageNumber">
      <span>{{ value }} of {{ total }}</span>
      <template #input>
        <div class="mt-4 title">Move Page</div>
        <v-text-field
          v-model="editedPage"
          :rules="rules"
          :label="$t('generic.edit')"
          single-line
          counter
          autofocus
        />
      </template>
    </v-edit-dialog>
    <v-btn
      v-shortkey.once="['shift', 'arrowleft']"
      :disabled="isFirstPage"
      text
      fab
      small
      @shortkey="firstPage"
      @click="firstPage"
    >
      <v-icon>{{ mdiPageFirst }}</v-icon>
    </v-btn>
    <v-btn
      v-shortkey.once="['arrowleft']"
      :disabled="isFirstPage"
      text
      fab
      small
      @shortkey="prevPage"
      @click="prevPage"
    >
      <v-icon>{{ mdiChevronLeft }}</v-icon>
    </v-btn>
    <v-btn
      v-shortkey.once="['arrowright']"
      :disabled="isLastPage"
      text
      fab
      small
      @shortkey="nextPage"
      @click="nextPage"
    >
      <v-icon>{{ mdiChevronRight }}</v-icon>
    </v-btn>
    <v-btn
      v-shortkey.once="['shift', 'arrowright']"
      :disabled="isLastPage"
      text
      fab
      small
      @shortkey="lastPage"
      @click="lastPage"
    >
      <v-icon>{{ mdiPageLast }}</v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiPageFirst, mdiPageLast, mdiChevronLeft, mdiChevronRight } from '@mdi/js'

export default Vue.extend({
  props: {
    value: {
      type: Number,
      default: 1,
      required: true
    },
    total: {
      type: Number,
      default: 1,
      required: true
    }
  },

  data() {
    return {
      editedPage: '1',
      rules: [
        (v: string) =>
          (v && parseInt(v, 10) > 0 && parseInt(v, 10) <= this.total) || 'Invalid page number!'
      ],
      mdiPageFirst,
      mdiPageLast,
      mdiChevronLeft,
      mdiChevronRight
    }
  },

  computed: {
    isFirstPage(): boolean {
      return this.value === 1
    },
    isLastPage(): boolean {
      return this.value === this.total || this.total === 0
    }
  },

  methods: {
    changePageNumber() {
      if (!this.editedPage) {
        return
      }
      const page = parseInt(this.editedPage, 10)
      if (page < 0 || page > this.total) {
        return
      }
      this.$emit('click:jump', page)
    },
    prevPage() {
      if (this.value === 1) {
        return
      }
      this.$emit('click:prev')
    },
    nextPage() {
      if (this.value === this.total) {
        return
      }
      this.$emit('click:next')
    },
    firstPage() {
      this.$emit('click:first')
    },
    lastPage() {
      this.$emit('click:last')
    }
  }
})
</script>
