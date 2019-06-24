import Vue from 'vue';
import HTTP from './http';

import { toPercent, toFixed, parseDate } from './filters'

Vue.filter('toPercent', toPercent)
Vue.filter('toFixed', toFixed)
Vue.filter('parseDate', parseDate)

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    labelers: {},
    matrix: null,
    usersAgreement: {}
  },

  computed: {
    matrixSrc() {
      return `data:image/png;base64, ${this.matrix}`
    }
  },
  
  methods: {
    goToUser(user) {
      window.location.href = `${window.location.href}${user.id}`
    }
  },
  created() {
    HTTP.get('labelers').then((response) => {
      this.num_truth_annotations = response.data.num_truth_annotations;
      this.labelers = response.data.users;
      this.matrix = response.data.matrix;
      this.usersAgreement = response.data.users_agreement
    });
  },
  watch: {
  }
});
