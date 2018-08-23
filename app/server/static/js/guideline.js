import Vue from 'vue';
import HTTP from './http';

const vm = new Vue({
  el: '#editor',
  data: {
    input: '# hello',
    project: Object,
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
    update: _.debounce(function(e) {
      this.input = e.target.value;
      this.project.guideline = this.input;
      HTTP.put('', this.project).then((response) => {
        this.project = response.data;
      });
    }, 300),
  },

});
