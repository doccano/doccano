import Vue from 'vue';
import { demoNamedEntity as data } from '../components/demo/demo_data';
import DemoApi from '../components/demo/demo_api';
import SequenceLabeling from '../components/sequence_labeling.vue';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

const demoApi = new DemoApi(data, 'start_offset');

new Vue({
  el: '#mail-app',

  components: { SequenceLabeling },

  beforeCreate() {
    demoApi.start();
  },

  beforeDestroy() {
    demoApi.stop();
  },

  template: '<SequenceLabeling />',
});
