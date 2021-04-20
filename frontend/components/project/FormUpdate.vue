<template>
  <v-card>
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
              v-model="project.enableRandomizeDocOrder"
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
              v-model="project.enableShareAnnotation"
              :label="$t('overview.shareAnnotations')"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import { projectNameRules, descriptionRules } from '@/rules/index'

export default {
  async fetch() {
    this.project = await this.$services.project.findById(this.projectId)
  },

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
    },
    projectId() {
      return this.$route.params.id
    }
  },

  watch: {
    'project.enableRandomizeDocOrder'() {
      this.doneEdit()
    },
    'project.enableShareAnnotation'() {
      this.doneEdit()
    }
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

    async doneEdit() {
      if (!this.validate()) {
        this.cancelEdit()
        return
      }
      try {
        await this.$services.project.update(this.project)
        this.beforeEditCache = {}
        this.$fetch()
      } finally {
        this.initEdit()
      }
    },

    validate() {
      return this.$refs.form.validate()
    }
  }
}
</script>
