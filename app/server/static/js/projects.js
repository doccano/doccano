import Vue from 'vue';
import Projects from './projects.vue';

new Vue({
  el: '#projects_root',

  components: { Projects },

  data: {
    djangoContext: {
      username: JSON.parse(document.getElementById('django.username').textContent),
      isSuperuser: JSON.parse(document.getElementById('django.is_superuser').textContent),
    },
  },

  template: '<Projects v-bind="djangoContext" />',
});
