import Vue from 'vue';
import HTTP from './http';

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
  },
  created() {
    HTTP.get('labelers').then((response) => {
      this.labelers = response.data.users;
      this.matrix = response.data.matrix;
      this.usersAgreement = response.data.users_agreement
    });
  },
  watch: {
  }
});
