import Vue from 'vue';
import vueDebounce from 'vue-debounce';
import SequenceLabeling from '../components/sequence_labeling.vue';

Vue.use(vueDebounce);
Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

new Vue({
  el: '#mail-app',

  components: { SequenceLabeling },

  template: '<SequenceLabeling />',
});
