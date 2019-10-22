import Vue from 'vue';
import Buefy from 'buefy';
import Users from '../components/users.vue';

Vue.use(Buefy);

new Vue({
  el: '#mail-app',

  components: { Users },

  template: '<Users />',
});
