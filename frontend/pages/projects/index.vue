<template>
  <v-content>
    <v-container
      fluid
      fill-height
    >
      <v-layout
        justify-center
      >
        <v-flex>
          <v-card>
            <v-card-title>
              <v-btn
                class="mb-2 text-capitalize"
                color="primary"
                @click="openAddModal"
              >
                Add Project
              </v-btn>
              <Modal
                ref="childDialogue"
                :title="addModal.title"
                :button="addModal.button"
                @agree="createProject"
              >
                <v-form
                  ref="form"
                  v-model="valid"
                  lazy-validation
                >
                  <v-text-field
                    v-model="newProject.name"
                    :rules="nameRules"
                    label="Project name"
                    prepend-icon="label"
                    required
                    autofocus
                  />
                  <v-text-field
                    v-model="newProject.description"
                    :rules="nameRules"
                    label="Description"
                    prepend-icon="label"
                    required
                  />
                  <v-select
                    v-model="newProject.project_type"
                    :items="projectTypes"
                    :rules="[v => !!v || 'Type is required']"
                    label="projectType"
                    prepend-icon="mdi-keyboard"
                    required
                  />
                </v-form>
              </Modal>
              <v-btn
                class="mb-2 ml-2 text-capitalize"
                outlined
                :disabled="selected.length === 0"
                @click="openRemoveModal"
              >
                Remove
              </v-btn>
              <Modal
                ref="removeDialogue"
                :title="removeModal.title"
                :button="removeModal.button"
                @agree="deleteProject"
              >
                Are you sure you want to remove these projects?
                <v-list dense>
                  <v-list-item v-for="(item, i) in selected" :key="i">
                    <v-list-item-content>
                      <v-list-item-title>{{ item.name }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </Modal>
            </v-card-title>
            <v-data-table
              v-model="selected"
              :headers="headers"
              :items="projects"
              :search="search"
              item-key="id"
              show-select
            >
              <template v-slot:top>
                <v-text-field
                  v-model="search"
                  prepend-inner-icon="search"
                  label="Search"
                  single-line
                  hide-details
                  filled
                />
              </template>
            </v-data-table>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import Modal from '~/components/Modal'
import ProjectService from '~/services/project.service'

export default {
  layout: 'projects',
  components: {
    Modal
  },
  data: () => ({
    dialog: false,
    valid: true,
    search: '',
    selected: [],
    selectedUser: null,
    projectTypes: [
      'Text Classification',
      'Sequence Labeling',
      'Sequence to sequence'
    ], // Todo: Get project types from backend server.
    projects: [],
    newProject: {
      name: '',
      description: '',
      project_type: null
    },
    addModal: {
      title: 'Add Project',
      button: 'Add Project'
    },
    removeModal: {
      title: 'Remove Project',
      button: 'Yes, remove'
    },
    headers: [
      {
        text: 'Name',
        align: 'left',
        value: 'name'
      },
      {
        text: 'Description',
        value: 'description'
      },
      {
        text: 'Type',
        value: 'project_type'
      }
    ],
    nameRules: [
      v => !!v || 'Name is required'
    ]
  }),

  async created() {
    this.projects = await ProjectService.getProjectList()
  },

  methods: {
    async createProject() {
      const response = await ProjectService.createProject(this.newProject)
      this.projects.unshift(response)
      this.newProject = {
        name: '',
        description: '',
        project_type: null
      }
    },
    async deleteProject() {
      // Todo: bulk delete.
      for (const project of this.selected) {
        await ProjectService.deleteProject(project.id)
        this.projects = this.projects.filter(item => item.id !== project.id)
      }
      this.selected = []
    },
    openAddModal() {
      this.$refs.childDialogue.open()
    },
    openRemoveModal() {
      this.$refs.removeDialogue.open()
    }
  }
}
</script>
