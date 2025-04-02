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
            class="elevation-0"
            @blur="editingSubject = false"
            @keyup.enter="editingSubject = false"
            autofocus
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
          class="custom-input"
          v-model="form.category"
          :items="categories"
          :label="$t('Category')"
          required
        />
        <v-textarea
          class="custom-input"
          v-model="form.text"
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
      <v-btn text @click="goBack">{{ $t('generic.cancel') }}</v-btn>
      <v-btn color="primary" :disabled="!isValid" @click="submitPerspective">
        {{ $t('generic.add') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiPencil } from '@mdi/js'
import { mapGetters } from 'vuex'

export default Vue.extend({
  name: 'CreatePerspective',
  layout: 'project',
  data() {
    return {
      mdiPencil,
      editingSubject: false,
      form: {
        subject: '',
        text: '',
        category: 'subjective'
      },
      categories: [
        { text: this.$t('Cultural'), value: 'cultural' },
        { text: this.$t('Technic'), value: 'technic' },
        { text: this.$t('Subjective'), value: 'subjective' }
      ],
      isValid: false,
      dbError: ""
    }
  },
  computed: {
    ...mapGetters('auth', ['getUsername']),
    userRole(): string {
      return this.$store.state.auth.role || 'annotator'
    }
  },
  methods: {
    async submitPerspective() {
      const projectId = Number(this.$route.params.id)
      const userId = this.$store.state.auth.id
      if (!userId) {
        console.error('User ID is missing. Ensure the user is logged in.')
        return
      }
      if (!this.form.text || !this.form.category || !this.form.subject) {
        console.error('Form is invalid. Ensure all required fields are filled.')
        return
      }
      const payload = {
        subject: this.form.subject,
        text: this.form.text,
        category: this.form.category,
        user: userId,
        project: projectId,
        roleOverride: true,
        role: this.userRole
      }
      
      console.log('Submitting perspective payload:', payload)
      try {
        await this.$repositories.perspective.create(projectId, payload)
        this.$router.push({
          path: '/message',
          query: {
            message: 'Perspective added successfully!',
            redirect: `/projects/${projectId}/perspectives`
          }
        })
      } catch (error: any) {
        console.error('Error submitting perspective:', error.response || error.message)
        this.dbError = "Can't access our database!"
      }
    },
    goBack() {
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