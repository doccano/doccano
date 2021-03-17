import Vue from 'vue';
import vueDebounce from 'vue-debounce';
import DocumentClassification from '../components/document_classification.vue';

Vue.use(vueDebounce);
Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

new Vue({
  el: '#mail-app',

  components: { DocumentClassification },

  template: '<DocumentClassification />',
});
