<template>
  <div class="v-data-footer">
    <v-edit-dialog
      large
      persistent
      @save="changePageNumber"
    >
      <span>{{ value }} of {{ length }}</span>
      <template v-slot:input>
        <div class="mt-4 title">
          Move Page
        </div>
      </template>
      <template v-slot:input>
        <v-text-field
          v-model="newPage"
          :rules="rules"
          label="Edit"
          single-line
          counter
          autofocus
        />
      </template>
    </v-edit-dialog>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-shortkey.once="['shift', 'arrowleft']"
          :disabled="value===1"
          text
          fab
          small
          v-on="on"
          @shortkey="firstPage"
          @click="firstPage"
        >
          <v-icon>mdi-page-first</v-icon>
        </v-btn>
      </template>
      <span>
        <v-icon>mdi-page-first</v-icon>
      </span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-shortkey.once="['arrowleft']"
          :disabled="value===1"
          text
          fab
          small
          v-on="on"
          @shortkey="prevPage"
          @click="prevPage"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </template>
      <span>←</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-shortkey.once="['arrowright']"
          :disabled="value===length || length===0"
          text
          fab
          small
          v-on="on"
          @shortkey="nextPage"
          @click="nextPage"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </template>
      <span>→</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-shortkey.once="['shift', 'arrowright']"
          :disabled="value===length || length===0"
          text
          fab
          small
          v-on="on"
          @shortkey="lastPage"
          @click="lastPage"
        >
          <v-icon>mdi-page-last</v-icon>
        </v-btn>
      </template>
      <span>
        <v-icon>mdi-page-last</v-icon>
      </span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Number,
      default: 1,
      required: true
    },
    length: {
      type: Number,
      default: 1,
      required: true
    }
  },
  data() {
    return {
      editedPage: null,
      rules: [
        v => (v && parseInt(v, 10) > 0 && parseInt(v, 10) <= this.length) || 'Invalid page number!'
      ]
    }
  },

  computed: {
    newPage: {
      get() {
        return this.value
      },
      set(newValue) {
        const value = parseInt(newValue, 10)
        this.editedPage = value
      }
    }
  },

  methods: {
    changePageNumber() {
      if (!this.editedPage || this.editedPage < 0 || this.editedPage > this.length) {
        return
      }
      this.$emit('input', this.editedPage)
    },
    prevPage() {
      const page = Math.max(this.value - 1, 1)
      this.$emit('input', page)
    },
    nextPage() {
      const page = Math.min(this.value + 1, this.length)
      this.$emit('input', page)
    },
    firstPage() {
      this.$emit('input', 1)
    },
    lastPage() {
      this.$emit('input', this.length)
    }
  }
}
</script>
