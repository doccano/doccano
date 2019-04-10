<template>
<div v-cloak>
  <section class="hero project-image">
    <div class="container">
      <div class="columns">
        <div class="column is-10 is-offset-1">
          <h1 class="title is-1 has-text-white">
            Hello, {{ username | title }}.
          </h1>
          <h2 class="subtitle is-4 has-text-white">
            I hope you are having a great day!
          </h2>
          <p v-if="isSuperuser">
            <a class="button is-medium is-primary" @click="isActive=!isActive">
              Create Project
            </a>
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Modal card for creating project. -->
  <div class="modal" :class="{ 'is-active': isActive }">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Create Project</p>
        <button class="delete" aria-label="close" @click="isActive=!isActive"></button>
      </header>
      <section class="modal-card-body">
        <div class="field">
          <label class="label">Project Name</label>
          <div class="control">
            <input class="input" type="text" required placeholder="Project name"
              v-model="projectName">
          </div>
          <p class="help is-danger">{{ projectNameError }}</p>
        </div>
        <div class="field">
          <label class="label">Description</label>
          <div class="control">
            <textarea class="textarea" required placeholder="Project description"
              v-model="description"></textarea>
          </div>
          <p class="help is-danger">{{ descriptionError }}</p>
        </div>
        <div class="field">
          <label class="label">Project Type</label>
          <div class="control">
            <select name="project_type" required v-model='projectType'>
              <option value="" selected="selected">---------</option>
              <option value="DocumentClassification">document classification</option>
              <option value="SequenceLabeling">sequence labeling</option>
              <option value="Seq2seq">sequence to sequence</option>
            </select>
          </div>
          <p class="help is-danger">{{ projectTypeError }}</p>
        </div>
      </section>
      <footer class="modal-card-foot pt20 pb20 pr20 pl20 has-background-white-ter">
        <button class="button is-primary" @click="create()">Create</button>
        <button class="button" @click="isActive=!isActive">Cancel</button>
      </footer>
    </div>
  </div>

  <div class="modal" :class="{ 'is-active': isDelete }">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Delete Project</p>
        <button class="delete" aria-label="close" @click="isDelete=!isDelete"></button>
      </header>
      <section class="modal-card-body">
        Are you sure you want to delete project?
      </section>
      <footer class="modal-card-foot pt20 pb20 pr20 pl20 has-background-white-ter">
        <button class="button is-danger" @click="deleteProject()">Delete</button>
        <button class="button" @click="isDelete=!isDelete">Cancel</button>
      </footer>
    </div>
  </div>

  <section class="hero">
    <div class="container">
      <div class="columns">
        <div class="column is-10 is-offset-1">
      <div class="card events-card">
        <header class="card-header">
          <p class="card-header-title">
            {{ items.length }} Projects
          </p>
          <div class="field card-header-icon">
            <div class="control">
              <div class="select">
                <select v-model="selected">
                  <option selected>All Project</option>
                  <option>Text Classification</option>
                  <option>Sequence Labeling</option>
                  <option>Seq2seq</option>
                </select>
              </div>
            </div>
          </div>
        </header>
        <div class="card-table">
          <div class="content">
            <table class="table is-fullwidth">
              <tbody>
                <tr v-for="project in selectedProjects" :key="project.id">
                  <td class="pl15r">
                    <div class="thumbnail-wrapper is-vertical">
                      <img class="project-thumbnail" :src="project.image">
                    </div>
                    <div class="dataset-item__main is-vertical">
                      <div class="dataset-item__main-title">
                        <div class="dataset-item__main-title-link dataset-item__link">
                          <a :href="'/projects/' + project.id" class="has-text-black">
                            {{ project.name }}
                          </a>
                        </div>
                      </div>
                      <div class="dataset-item__main-subtitle">
                        {{ project.description }}
                      </div>
                      <div class="dataset-item__main-info">
                        <span class="dataset-item__main-update">
                          updated <span>{{ project.updated_at | daysAgo }}</span>
                        </span>
                      </div>
                    </div>
                  </td>
                  <td class="is-vertical">
                    <span class="tag is-normal">{{ project.project_type }}</span>
                  </td>
                  <td v-if="isSuperuser" class="is-vertical">
                    <a :href="'/projects/' + project.id + '/docs'">Edit</a>
                  </td>
                  <td v-if="isSuperuser" class="is-vertical">
                    <a class="has-text-danger" @click="setProject(project)">Delete</a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      </div>
      </div>
    </div>
  </section>

</div>
</template>

<script>
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');

export default {
  props: {
    username: {
      type: String,
      required: true,
    },
    isSuperuser: {
      type: Boolean,
      default: false,
    },
  },

  filters: {
    title: (value) => {
      const string = (value || '').toString();
      return string.charAt(0).toUpperCase() + string.slice(1);
    },

    daysAgo: (dateStr) => {
      const updatedAt = new Date(dateStr);
      const currentTm = new Date();

      // difference between days(ms)
      const msDiff = currentTm.getTime() - updatedAt.getTime();

      // convert daysDiff(ms) to daysDiff(day)
      const daysDiff = Math.floor(msDiff / (1000 * 60 * 60 * 24));

      return daysDiff === 1
        ? `${daysDiff} day ago`
        : `${daysDiff} days ago`;
    },
  },

  data: () => ({
    items: [],
    isActive: false,
    isDelete: false,
    project: null,
    selected: 'All Project',
    projectName: '',
    description: '',
    projectType: '',
    descriptionError: '',
    projectTypeError: '',
    projectNameError: '',
  }),

  methods: {

    deleteProject() {
      axios.delete(`${baseUrl}/v1/projects/${this.project.id}`).then(() => {
        this.isDelete = false;
        const index = this.items.indexOf(this.project);
        this.items.splice(index, 1);
      });
    },

    setProject(project) {
      this.project = project;
      this.isDelete = true;
    },

    matchType(projectType) {
      if (projectType === 'DocumentClassification') {
        return this.selected === 'Text Classification';
      }
      if (projectType === 'SequenceLabeling') {
        return this.selected === 'Sequence Labeling';
      }
      if (projectType === 'Seq2seq') {
        return this.selected === 'Seq2seq';
      }
      return false;
    },

    create() {
      const payload = {
        name: this.projectName,
        description: this.description,
        project_type: this.projectType,
        guideline: 'Please write annotation guideline.',
        resourcetype: this.resourceType(),
      };
      axios.post(`${baseUrl}/v1/projects`, payload)
        .then((response) => {
          window.location = `${baseUrl}/projects/${response.data.id}/docs/create`;
        })
        .catch((error) => {
          this.projectTypeError = '';
          this.projectNameError = '';
          this.descriptionError = '';
          if ('resourcetype' in error.response.data) {
            this.projectTypeError = error.response.data.resourcetype;
          }
          if ('name' in error.response.data) {
            this.projectNameError = error.response.data.name[0];
          }
          if ('description' in error.response.data) {
            this.descriptionError = error.response.data.description[0];
          }
        });
    },

    resourceType() {
      if (this.projectType === 'DocumentClassification') {
        return 'TextClassificationProject';
      }
      if (this.projectType === 'SequenceLabeling') {
        return 'SequenceLabelingProject';
      }
      if (this.projectType === 'Seq2seq') {
        return 'Seq2seqProject';
      }
      return '';
    },
  },

  computed: {
    selectedProjects() {
      return this.items.filter(item => this.selected === 'All Project' || this.matchType(item.project_type));
    },
  },

  created() {
    axios.get(`${baseUrl}/v1/projects`).then((response) => {
      this.items = response.data;
    });
  },
};
</script>
