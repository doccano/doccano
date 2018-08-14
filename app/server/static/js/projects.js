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
    selectedType: 'All',
    isActive: false,
    isDelete: false,
  },

  methods: {
    getProjects() {
      axios.get(`${baseUrl}/api/projects`).then((response) => {
        this.items = response.data;
      });
    },

    deleteProject(project) {
      axios.delete(`${baseUrl}/api/projects/${project.id}/`).then((response) => {
        this.isDelete = false;
        const index = this.items.indexOf(project);
        this.items.splice(index, 1);
      });
    },

    updateSelectedType(type) {
      this.selectedType = type;
    },
  },

  computed: {
    uniqueProjectTypes() {
      const types = [];
      for (let i = 0; i < this.items.length; i++) {
        const item = this.items[i];
        types.push(item.project_type);
      }
      const uniqueTypes = Array.from(new Set(types));

      return uniqueTypes;
    },

    filteredProjects() {
      // filter projects
      const projects = [];
      for (let i = 0; i < this.items.length; i++) {
        const item = this.items[i];
        if ((this.selectedType === 'All') || (item.project_type === this.selectedType)) {
          projects.push(item);
        }
      }
      // create nested projects
      const nestedProjects = [];
      for (let i = 0; i < Math.ceil(projects.length / 3); i++) {
        const p = projects.slice(i * 3, (i + 1) * 3);
        nestedProjects.push(p);
      }
      return nestedProjects;
    },
  },

  created() {
    this.getProjects();
  },
});
