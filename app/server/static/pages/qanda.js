import Vue from 'vue';
import QandA from '../components/question_and_answer.vue';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

new Vue({
  el: '#mail-app',

  components: { QandA },

  template: '<QandA />',
});
