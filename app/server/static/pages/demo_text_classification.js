import Vue from 'vue';
import DemoTextClassification from '../components/demo/demo_text_classification.vue';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

new Vue({
  el: '#mail-app',

  components: { DemoTextClassification },

  template: '<DemoTextClassification />',
});
