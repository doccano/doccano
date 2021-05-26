import Vue from 'vue';
import { demoTextClassification as data } from '../components/demo/demo_data';
import DemoApi from '../components/demo/demo_api';
import DocumentClassification from '../components/document_classification.vue';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

const demoApi = new DemoApi(data, 'label');

new Vue({
  el: '#mail-app',

  components: { DocumentClassification },

  beforeCreate() {
    demoApi.start();
  },

  beforeDestroy() {
    demoApi.stop();
  },

  template: '<DocumentClassification />',
});
