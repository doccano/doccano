import Vue from 'vue';
import { demoTextSimilarity as data } from '../components/demo/demo_data';
import DemoApi from '../components/demo/demo_api';
import DocumentSimilarity from '../components/document_similarity.vue';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

const demoApi = new DemoApi(data, 'label');

new Vue({
  el: '#mail-app',

  components: { DocumentSimilarity },

  beforeCreate() {
    demoApi.start();
  },

  beforeDestroy() {
    demoApi.stop();
  },

  template: '<DocumentSimilarity />',
});
