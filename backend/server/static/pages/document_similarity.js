import Vue from 'vue';
import vueDebounce from 'vue-debounce';
import DocumentSimilarity from '../components/document_similarity.vue';

Vue.use(vueDebounce);
Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

new Vue({
  el: '#mail-app',

  components: { DocumentSimilarity },

  template: '<DocumentSimilarity />',
});
