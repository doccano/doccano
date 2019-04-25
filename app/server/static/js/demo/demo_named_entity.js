import Vue from 'vue';
import DemoNamedEntity from './demo_named_entity.vue';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

new Vue({
  el: '#mail-app',

  components: { DemoNamedEntity },

  template: '<DemoNamedEntity />',
});
