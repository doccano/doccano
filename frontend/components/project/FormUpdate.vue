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
            <h3>Tags</h3>
            <v-chip
              v-for="tag in tags"
              :key="tag.id"
              close
              outlined
              @click:close="removeTag(tag.id)">{{tag.text}}
            </v-chip>
            <v-text-field
            v-model="tagInput"
            clearable
            prepend-icon="add_circle"
            @keyup.enter="addTag()"
            @click:prepend="addTag()">
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            sm="6"
          >
            <h3>Shuffle</h3>
            <v-checkbox
              v-model="project.enableRandomOrder"
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

  data() {
    return {
      project: {},
      tags: {},
      beforeEditCache: {},
      tagInput: '',
      edit: {
        name: false,
        desc: false
      },
      projectNameRules,
      descriptionRules,
      valid: false
    }
  },
  async fetch() {
    this.project = await this.$services.project.findById(this.projectId)
    this.getTags()
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
    'project.enableRandomOrder'() {
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
    },

    async getTags(){
        this.tags = await this.$services.tag.list(this.projectId)
    },

    addTag(){
      this.$services.tag.create(this.projectId, this.tagInput)
      this.tagInput = ''
      this.getTags()
    },

    removeTag(id){
      this.$services.tag.delete(this.projectId, id)
      this.tags = this.tags.filter(tag => tag.id !== id)
    }
  }
}
</script>
