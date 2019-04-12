import * as marked from 'marked';
import Vue from 'vue';
import vueDebounce from 'vue-debounce';
import HTTP from './http';

Vue.use(vueDebounce);

const vm = new Vue({ // eslint-disable-line no-unused-vars
  el: '#mail-app',
  data: {
    input: '',
    project: Object,
    messages: [],
  },

  computed: {
    compiledMarkdown() {
      return marked(this.input, {
        sanitize: true,
      });
    },
  },

  created() {
    HTTP.get().then((response) => {
      this.input = response.data.guideline;
      this.project = response.data;
    });
  },

  methods: {
    update(value) {
      this.input = value;
      const payload = {
        guideline: this.input,
      };
      HTTP.patch('', payload).then((response) => {
        this.project = response.data;
      });
    },
  },

});
