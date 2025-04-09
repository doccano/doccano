<template>
  <v-card>
    <v-alert v-if="dbError" type="error" dense>
      {{ dbError }}
    </v-alert>
    <v-card-title>
      <div>
        <template v-if="editingSubject">
          <v-text-field
            v-model="form.subject"
            label="Subject"
            dense
            solo
            hide-details
            autofocus
            class="elevation-0"
            @blur="editingSubject = false"
            @keyup.enter="editingSubject = false"
          />
        </template>
        <template v-else>
          <span class="headline" @click="editingSubject = true">
            {{ form.subject || 'Perspective Title' }}
            <v-icon class="edit-icon">{{ mdiPencil }}</v-icon>
          </span>
        </template>
      </div>
    </v-card-title>
    <v-card-text>
      <v-form ref="form" v-model="isValid">
        <v-select
          v-model="form.category"
          class="custom-input"
          :items="categories"
          :label="$t('Category')"
          required
        />
        <v-textarea
          v-model="form.text"
          class="custom-input"
          :label="$t('Text')"
          counter="2000"
          required
          rows="10"
          auto-grow
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="cancelEdit">{{ $t('generic.cancel') }}</v-btn>
      <v-btn color="primary" :disabled="!isValid" @click="submitEdit">
        {{ $t('generic.save') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
// @ts-nocheck
import Vue from 'vue'
import axios from 'axios'
import { mdiPencil } from '@mdi/js'
import { mapGetters } from 'vuex'
export default Vue.extend({
  name: 'EditPerspective',
  layout: 'project',
  data() {
    return {
      mdiPencil,
      editingSubject: false,
      isValid: false,
      form: {
        subject: '',
        text: '',
        category: 'subjective'
      },
      originalForm: {
        subject: '',
        text: '',
        category: 'subjective'
      },
      categories: [] as any[],
      dbError: ""
    }
  },
  computed: {
    ...mapGetters('auth', ['getUsername'])
  },
  mounted() {
    this.loadPerspective()
    this.fetchCategories()
  },
  methods: {
    loadPerspective() {
      const perspectiveId = this.$route.query.perspectiveId
      if (perspectiveId && this.$route.params.id) {
        axios.get(`/v1/projects/${this.$route.params.id}/perspectives/${perspectiveId}/`)
          .then((response: any) => {
            this.form = { ...response.data }
            this.originalForm = { ...response.data }
          })
          .catch(error => console.error('Erro ao buscar perspective:', error.response || error.message))
      }
    },
    fetchCategories() {
      this.categories = [
        { text: this.$t('Cultural'), value: 'cultural' },
        { text: this.$t('Technic'), value: 'technic' },
        { text: this.$t('Subjective'), value: 'subjective' }
      ]
    },
    submitEdit() {
      const perspectiveId = this.$route.query.perspectiveId
      if (perspectiveId && this.$route.params.id) {
        const patchData: any = {}
        if (this.form.subject !== this.originalForm.subject) {
          patchData.subject = this.form.subject
        }
        if (this.form.text !== this.originalForm.text) {
          patchData.text = this.form.text
        }
        if (this.form.category !== this.originalForm.category) {
          patchData.category = this.form.category
        }
        if (Object.keys(patchData).length === 0) {
          console.log("Nenhuma alteração realizada.")
          return
        }
        axios.patch(
          `/v1/projects/${this.$route.params.id}/perspectives/${perspectiveId}/`,
          patchData
        )
          .then(() => {
            this.$router.push({
              path: '/message',
              query: {
                message: 'Perspective updated successfully!',
                redirect: `/projects/${this.$route.params.id}/perspectives`
              }
            })
          })
          .catch(error => {
            console.error('Erro ao atualizar perspective:', error.response || error.message)
            this.dbError = "Can't access our database!"
          })
      }
    },
    cancelEdit() {
      this.$router.push(this.localePath(`/projects/${this.$route.params.id}/perspectives`))
    }
  }
})
</script>

<style scoped>
.v-card {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
}

.headline {
  cursor: pointer;
  font-weight: bold;
  font-size: 1.5rem;
  display: inline-flex;
  align-items: center;
}

.headline .edit-icon {
  opacity: 0;
  transition: opacity 0.3s;
  color: inherit;
  margin-left: 8px;
}

.headline:hover .edit-icon {
  opacity: 1;
}

::v-deep .custom-input .v-input__slot {
  background-color: #f0f0f0 !important;
  border-radius: 4px;
}
</style>