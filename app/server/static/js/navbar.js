import Vue from 'vue';
import axios from 'axios';
import * as bulmaToast from 'bulma-toast';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');

const projectSearch = window.location.href.match(/\/projects\/(\d+)\//);
let projectId = null
if (projectSearch && projectSearch.length > 1) {
  [, projectId] = projectSearch;
}


const vm = new Vue({
  el: '#navbar-component',
  delimiters: ['[[', ']]'],
  data() {
    return {
      modelProcessing: false,
    };
  },
  methods: {
    runModel() {
      if (this.modelProcessing || !projectId) {
        return;
      }
      this.modelProcessing = true;
      bulmaToast.toast({
        message: 'Processing...',
        type: 'is-info',
        position: 'top-center',
      });
      axios.get(`${baseUrl}/api/projects/${projectId}/runmodel/`).then(() => {
        this.modelProcessing = false;
        bulmaToast.toast({
          message: 'Successfully ran the model',
          type: 'is-success',
          position: 'top-center',
        });
      }).catch(() => {
        this.modelProcessing = false;
        bulmaToast.toast({
          message: 'An error occurred',
          type: 'is-danger',
          position: 'top-center',
        });
      });
    },
  },
});
