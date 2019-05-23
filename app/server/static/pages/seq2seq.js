import Vue from 'vue';
import Seq2Seq from '../components/seq2seq.vue';

Vue.use(require('vue-shortkey'));

new Vue({
  el: '#mail-app',

  components: { Seq2Seq },

  template: '<Seq2Seq />',
});
