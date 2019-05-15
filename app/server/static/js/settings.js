import Vue from 'vue';
import HTTP from './http';

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    projectSettings: {
        use_machine_model_sort: false,
        show_ml_model_prediction: false,
        enable_metadata_search: false,
        name: '',
        description: '',
        users: []
    },
    users: []
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

  async created() {
    const project = await HTTP.get('')
    this.setProjectSettings(project.data);

    const users = await HTTP.get('users');
    this.users = users.data;
  },

  computed: {
    submitDisabled () {
      return this.projectSettings.name.length === 0 || this.projectSettings.name.length > 100 || this.projectSettings.description.length === 0 || this.projectSettings.description.length > 500 || this.projectSettings.users.length === 0 
    }
  }
});
