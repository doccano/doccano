import Vue from 'vue';
import SequenceLabeling from './sequence_labeling.vue';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

new Vue({
  el: '#mail-app',

  components: { SequenceLabeling },

  template: '<SequenceLabeling />',
});
