<template>
  <v-card>
    <v-card-title class="mb-2">
      <h2>About project</h2>
    </v-card-title>
    <v-card-text v-if="isReady">
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-row>
          <v-col
            cols="12"
            sm="6"
          >
            <h3>Name</h3>
            <v-text-field
              v-model="project.name"
              label="Add project name"
              :rules="projectNameRules($t('rules.projectNameRules'))"
              :disabled="!edit.name"
              single-line
            />
          </v-col>
          <v-col
            cols="12"
            sm="6"
          >
            <v-btn
              v-if="!edit.name"
              outlined
              color="grey"
              class="text-capitalize"
              @click="editProject('name')"
            >
              Edit
            </v-btn>
            <v-btn
              v-if="edit.name"
              outlined
              color="primary"
              class="text-capitalize"
              @click="doneEdit()"
            >
              Save
            </v-btn>
            <v-btn
              v-if="edit.name"
              outlined
              color="grey"
              class="text-capitalize"
              @click="cancelEdit()"
            >
              Cancel
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            sm="6"
          >
            <h3>Description</h3>
            <v-text-field
              v-model="project.description"
              label="Add description"
              :rules="descriptionRules($t('rules.descriptionRules'))"
              :disabled="!edit.desc"
              single-line
            />
          </v-col>
          <v-col
            cols="12"
            sm="6"
          >
            <v-btn
              v-if="!edit.desc"
              outlined
              color="grey"
              class="text-capitalize"
              @click="editProject('desc')"
            >
              Edit
            </v-btn>
            <v-btn
              v-if="edit.desc"
              outlined
              color="primary"
              class="text-capitalize"
              @click="doneEdit()"
            >
              Save
            </v-btn>
            <v-btn
              v-if="edit.desc"
              outlined
              color="grey"
              class="text-capitalize"
              @click="cancelEdit()"
            >
              Cancel
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            sm="6"
          >
            <h3>Shuffle</h3>
            <v-checkbox
              v-model="project.randomize_document_order"
              :label="$t('overview.randomizeDocOrder')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            sm="6"
          >
            <h3>Collaboration</h3>
            <v-checkbox
              v-model="project.collaborative_annotation"
              :label="$t('overview.shareAnnotations')"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import ProjectService from '@/services/project.service'
import { projectNameRules, descriptionRules } from '@/rules/index'

export default {
  layout: 'project',

  data() {
    return {
      project: {},
      beforeEditCache: {},
      edit: {
        name: false,
        desc: false
      },
      projectNameRules,
      descriptionRules,
      valid: false
    }
  },

  computed: {
    isReady() {
      return !!this.project
    }
  },

  watch: {
    'project.randomize_document_order'() {
      this.doneEdit()
    },
    'project.collaborative_annotation'() {
      this.doneEdit()
    }
  },

  created() {
    const projectId = this.$route.params.id
    ProjectService.fetchProjectById(projectId)
      .then((response) => {
        this.project = response.data
      })
      .catch((error) => {
        alert(error)
      })
  },

  methods: {
    initEdit() {
      Object.keys(this.edit).forEach((v) => { this.edit[v] = false })
    },

    editProject(name) {
      this.cancelEdit()
      this.edit[name] = true
      Object.assign(this.beforeEditCache, this.project)
    },

    cancelEdit() {
      this.initEdit()
      Object.assign(this.project, this.beforeEditCache)
    },

    doneEdit() {
      if (!this.validate()) {
        this.cancelEdit()
        return
      }
      const projectId = this.$route.params.id
      ProjectService.updateProject(projectId, this.project)
        .then((response) => {
          this.project = response.data
          this.beforeEditCache = {}
        })
        .catch((error) => {
          alert(error)
        })
        .finally(() => {
          this.initEdit()
        })
    },

    validate() {
      return this.$refs.form.validate()
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
