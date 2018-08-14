import { HorizontalBar, mixins, Doughnut } from 'vue-chartjs';
import axios from 'axios';
import Vue from 'vue';

const { reactiveProp, reactiveData } = mixins;

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseURL = window.location.href.split('/').slice(3, 5).join('/');
const HTTP = axios.create({
  baseURL: `/api/${baseURL}/`,
});


Vue.component('line-chart', {
  extends: HorizontalBar,
  mixins: [reactiveProp],
  props: ['chartData'],
  data() {
    return {
      options: {
        scales: {
          yAxes: [{
            barPercentage: 0.3,
          }],
          xAxes: [{
            ticks: {
              beginAtZero: true,
              min: 0,
            },
          }],
        },
        maintainAspectRatio: false,
      },
    };
  },

  mounted() {
    this.renderChart(this.chartData, this.options);
  },
});


Vue.component('doughnut-chart', {
  extends: Doughnut,
  mixins: [reactiveProp],
  props: ['chartData'],
  data() {
    return {
      options: {
        maintainAspectRatio: false,
      },
    };
  },

  mounted() {
    this.renderChart(this.chartData, this.options);
  },
});

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    labelData: null,
    userData: null,
    progressData: null,
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
  },
});
