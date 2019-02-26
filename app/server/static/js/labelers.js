import Vue from 'vue';
import HTTP from './http';

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    labelers: {},
    matrix: null
  },

  computed: {
  },
  
  methods: {
  },
  created() {
    HTTP.get('labelers').then((response) => {
      this.labelers = response.data.users;
      this.matrix = response.data.matrix;
    });
  },
  watch: {
  }
});
