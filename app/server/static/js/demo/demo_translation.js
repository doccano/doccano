import Vue from 'vue';
import DemoTranslation from './demo_translation.vue';

Vue.use(require('vue-shortkey'));

new Vue({
  el: '#mail-app',

  components: { DemoTranslation },

  template: '<DemoTranslation />',
});
