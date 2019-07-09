import Vue from 'vue';
import { demoTranslation as data } from '../components/demo/demo_data';
import DemoApi from '../components/demo/demo_api';
import Seq2Seq from '../components/seq2seq.vue';

Vue.use(require('vue-shortkey'));

const demoApi = new DemoApi(data, 'text');

new Vue({
  el: '#mail-app',

  components: { Seq2Seq },

  beforeCreate() {
    demoApi.start();
  },

  beforeDestroy() {
    demoApi.stop();
  },

  template: '<Seq2Seq />',
});
