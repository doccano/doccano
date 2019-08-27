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
                @click="dialog=true"
              >
                Add Project
              </v-btn>
              <v-dialog
                v-model="dialog"
                width="800px"
              >
                <form-project-creation @cancel="dialog=false" @create-project="createProject" />
              </v-dialog>
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
import FormProjectCreation from '~/components/FormProjectCreation'
import ProjectService from '~/services/project.service'

export default {
  layout: 'projects',
  components: {
    Modal,
    FormProjectCreation
  },
  data: () => ({
    dialog: false,
    search: '',
    selected: [],
    selectedUser: null,
    projects: [],
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
    ]
  }),

  async created() {
    this.projects = await ProjectService.getProjectList()
  },

  methods: {
    createProject(project) {
      this.projects.unshift(project)
      this.dialog = false
    },
    async deleteProject() {
      // Todo: bulk delete.
      for (const project of this.selected) {
        await ProjectService.deleteProject(project.id)
        this.projects = this.projects.filter(item => item.id !== project.id)
      }
      this.selected = []
    },
    openRemoveModal() {
      this.$refs.removeDialogue.open()
    }
  }
}
</script>
