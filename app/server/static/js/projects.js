import Vue from 'vue';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');


const vm = new Vue({
  el: '#projects_root',
  delimiters: ['[[', ']]'],
  data: {
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
  },

  methods: {

    deleteProject() {
      axios.delete(`${baseUrl}/v1/projects/${this.project.id}`).then((response) => {
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

    getDaysAgo(dateStr) {
      const updatedAt = new Date(dateStr);
      const currentTm = new Date();

      // difference between days(ms)
      const msDiff = currentTm.getTime() - updatedAt.getTime();

      // convert daysDiff(ms) to daysDiff(day)
      const daysDiff = Math.floor(msDiff / (1000 * 60 * 60 * 24));

      return daysDiff;
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
      const projects = [];
      for (let item of this.items) {
        if ((this.selected === 'All Project') || this.matchType(item.project_type)) {
          projects.push(item);
        }
      }
      return projects;
    },
  },

  created() {
    axios.get(`${baseUrl}/v1/projects`).then((response) => {
      this.items = response.data;
    });
  },
});
