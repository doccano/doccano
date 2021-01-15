import Vue from 'vue';
import vueDebounce from 'vue-debounce';
import Speech2text from '../components/speech2text.vue';

Vue.use(require('vue-shortkey'));

Vue.use(vueDebounce);

new Vue({
  el: '#mail-app',

  components: { Speech2text },

  template: '<Speech2text />',
});
