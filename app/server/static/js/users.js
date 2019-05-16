import Vue from 'vue';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');


const vm = new Vue({
  el: '#users_root',
  delimiters: ['[[', ']]'],
  data: {
    items: [],
    isActive: false,
    isDelete: false,
    user: null
  },

  methods: {

    deleteUser() {
      axios.delete(`${baseUrl}/api/users/${this.user.id}/`).then((response) => {
        this.isDelete = false;
        const index = this.items.indexOf(this.user);
        this.items.splice(index, 1);
      });
    },

    setUser(user) {
      this.user = user;
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
    axios.get(`${baseUrl}/api/users/`).then((response) => {
      this.items = response.data;
    });

    
  },

  mounted() {
    if (this.$refs.formError.value === 'true') {
      this.isActive = true
    }
  }
});
