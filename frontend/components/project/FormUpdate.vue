<template>
  <v-card>
    <v-card-text v-if="!!project">
      <!-- Project Status Indicator -->
      <v-alert 
        v-if="project.status"
        :type="(project.isOpen !== undefined ? project.isOpen : true) ? 'info' : 'warning'"
        outlined
        dense
        class="mb-4"
      >
        <div class="d-flex align-center">
          <v-icon small class="mr-2">
            {{ (project.isOpen !== undefined ? project.isOpen : true) ? 'mdi-lock-open' : 'mdi-lock' }}
          </v-icon>
          <span class="text-body-2">
            <strong>Project Status:</strong> 
            {{ (project.isOpen !== undefined ? project.isOpen : true) ? 'Open' : 'Closed' }} 
            (Version {{ project.currentVersion || 1 }})
          </span>
          <v-spacer />
          <v-btn 
            text 
            small 
            color="primary"
            @click="$router.push(`/projects/${$route.params.id}/settings?tab=tab-versions`)"
          >
            Manage Versions
          </v-btn>
        </div>
        <div class="text-caption mt-1" style="opacity: 0.8;">
          {{ (project.isOpen !== undefined ? project.isOpen : true) ? 'Users can annotate examples' : 'Project is in discussion/voting phase' }}
        </div>
      </v-alert>

      <v-form ref="form" v-model="valid" :disabled="!isEditing">
        <v-row>
          <v-col cols="12" sm="12" md="6" lg="6" xl="6">
            <project-name-field v-model="project.name" />
            <project-description-field v-model="project.description" />
            <tag-list v-model="tags" />
            <random-order-field v-model="project.enableRandomOrder" />
            <sharing-mode-field v-model="project.enableSharingMode" />
            <v-checkbox
              v-if="project.canDefineLabel"
              v-model="project.allowMemberToCreateLabelType"
              label="Allow project members to create label types"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions class="ps-4 pt-0">
      <v-btn v-if="!isEditing" color="primary" class="text-capitalize" @click="isEditing = true">
        Edit
      </v-btn>
      <v-btn
        v-show="isEditing"
        color="primary"
        :disabled="!valid || isUpdating"
        class="mr-4 text-capitalize"
        @click="save"
      >
        {{ $t('generic.save') }}
      </v-btn>
      <v-btn v-show="isEditing" :disabled="isUpdating" class="text-capitalize" @click="cancel">
        {{ $t('generic.cancel') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import ProjectDescriptionField from './ProjectDescriptionField.vue'
import ProjectNameField from './ProjectNameField.vue'
import RandomOrderField from './RandomOrderField.vue'
import SharingModeField from './SharingModeField.vue'
import TagList from './TagList.vue'
import { Project } from '~/domain/models/project/project'

export default Vue.extend({
  components: {
    ProjectNameField,
    ProjectDescriptionField,
    RandomOrderField,
    SharingModeField,
    TagList
  },

  data() {
    return {
      project: {} as Project,
      tags: [] as string[],
      valid: false,
      isEditing: false,
      isUpdating: false
    }
  },

  async fetch() {
    const projectId = this.$route.params.id
    this.project = await this.$services.project.findById(projectId)
    this.tags = this.project.tags.map((item) => item.text)
    this.isEditing = false
  },

  methods: {
    cancel() {
      this.$fetch()
    },

    async save() {
      this.isUpdating = true
      await this.$services.project.update(this.project.id, this.project)
      await this.$services.tag.bulkUpdate(this.project.id, this.tags)
      this.$fetch()
      this.isUpdating = false
    }
  }
})
</script>
