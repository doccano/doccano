import Vue from 'vue';
import DocumentClassification from '../../document_classification.vue';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

new Vue({
  el: '#mail-app',

  components: { DocumentClassification },

  template: '<DocumentClassification />',
});
