import Vue from 'vue';
import HTTP from './http';

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    projectSettings: {
        use_machine_model_sort: false
    }
  },

  methods: {
      submit() {
          HTTP.patch('', this.projectSettings).then((response) => {
          })
      },
      setProjectSettings(data) {
        Object.keys(this.projectSettings).forEach((key) => {
            this.projectSettings[key] = data[key]
        })
      }
  },

  created() {
    HTTP.get('').then((response) => {
        this.setProjectSettings(response.data);
    });
  },
});
