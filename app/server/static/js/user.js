import Vue from 'vue';
import HTTP from './http';

import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');

function validateEmail(email) 
{
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

const vm = new Vue({
  el: '#users_root',
  delimiters: ['[[', ']]'],
  data: {
    userSettings: {
        username: '',
        email: '',
        projects: []
    },
    projects: [],
    isDelete: false
  },

  methods: {
      submit() {
          HTTP.patch('', this.userSettings).then((response) => {
          })
      },
      setUserSettings(data) {
        Object.keys(this.userSettings).forEach((key) => {
            this.userSettings[key] = data[key]
        })
      }
  },

  async created() {
    const user = await HTTP.get('')
    this.setUserSettings(user.data);

    const projects = await axios.get(`${baseUrl}/api/projects/`)
    this.projects = projects.data;
  },

  computed: {
    submitDisabled () {
      return this.userSettings.username.length === 0 || this.userSettings.username.length > 100 || (this.userSettings.email.length > 0 && !validateEmail(this.userSettings.email))
    }
  }
});
