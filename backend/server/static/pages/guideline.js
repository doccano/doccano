import Vue from 'vue';
import vueDebounce from 'vue-debounce';
import Guideline from '../components/guideline.vue';

Vue.use(vueDebounce);

new Vue({
  el: '#mail-app',

  components: { Guideline },

  template: '<Guideline />',
});
