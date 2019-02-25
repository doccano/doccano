import Vue from 'vue';
import HTTP from './http';

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    labelers: {},
  },

  computed: {
  },
  
  methods: {
  },
  created() {
    HTTP.get('labelers').then((response) => {
      this.labelers = response.data.users;
    });
  },
  watch: {
  }
});
