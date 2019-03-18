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
    agreementTable() {
      const data = []
      let header = []
      for (let key in this.matrix) {
        header.push(key)
        data.push(this.matrix[key])
      }

      header = header.map((th) => {
        const labeler = this.labelers.find((l) => +l.id === +th)
        return labeler.name
      })
      return { data, header }
    }
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
