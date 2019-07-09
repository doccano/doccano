import { HorizontalBar, mixins, Doughnut } from 'vue-chartjs';
import Vue from 'vue';
import HTTP from './http';

import { VueGoodTable } from 'vue-good-table';

import { toFixed } from './filters'

import 'vue-good-table/dist/vue-good-table.css'

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

Vue.filter('toFixed', toFixed)

const { reactiveProp, reactiveData } = mixins;

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[[[', ']]]]'],
  data: {
    labelData: null,
    userData: null,
    progressData: null,
    showRunModel: false,
    classWeightsData: [],
    classWeightsColumns: [
      {
        label: 'Term',
        field: 'term'
      },
      {
        label: 'Weight',
        field: 'weight',
        type: 'number'
      },
      {
        label: 'Label',
        field: 'label',
        type: 'number'
      },
    ]
  },

  components: {
    VueGoodTable
  },

  methods: {
    makeData(data, labels, label) {
      const res = {
        labels: labels,
        datasets: [{
          label: label,
          backgroundColor: '#00d1b2',
          data: data,
        }],
      };
      return res;
    },
    runModel() {
        if (this.modelProcessing || !projectId) {
          return;
        }
        this.modelProcessing = true;
        bulmaToast.toast({
          message: 'Processing...',
          type: 'is-info',
          position: 'top-center'
        });
        axios.get(`${baseUrl}/api/projects/${projectId}/runmodel/`).then((r) => {
          this.modelProcessing = false;
          this.showRunModel = true;
          bulmaToast.toast({
            message: 'Successfully ran the model',
            type: 'is-success',
            position: 'top-center',
          });
          this.resultSplitted = r.data.result.replace(/\n/g, '<br>');
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

  created() {
    HTTP.get('stats').then((response) => {
      this.labelData = this.makeData(response.data.label.data, response.data.label.labels, 'Label stats');
      this.userData = this.makeData(response.data.user.data, response.data.user.users, 'User stats');
    });
    HTTP.get('progress').then((response) => {
      const complete = response.data.total - response.data.remaining;
      const incomplete = response.data.remaining;
      this.progressData = {
        datasets: [{
          data: [complete, incomplete],
          backgroundColor: ['#00d1b2', '#ffdd57'],
        }],

        labels: [
          'Completed',
          'Incomplete',
        ],
      };
    });
    HTTP.get('class_weights').then((response) => {
      const weightsData = response.data.weights
      const threshold = 0
      for (let i = 0, l = weightsData.length; i < l; i++) {
        if (weightsData[i][1] <= -threshold || weightsData[i][1] >= threshold) {
          this.classWeightsData.push({
            term: weightsData[i][0],
            weight: +weightsData[i][1],
            label: +weightsData[i][2]
          })
        }
      }

      this.classWeightsData = this.classWeightsData.sort((a, b) => {
        if (a.weight > b.weight) {
          return -1
        } else if (a.weight < b.weight) {
          return 1
        }

        return 0
      })
    });
  },
});
