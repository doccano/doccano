/* global _:readonly */
/* global marked:readonly */

import Vue from 'vue';
import HTTP from './http';

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
    update: _.debounce((e) => {
      this.input = e.target.value;
      const payload = {
        guideline: this.input,
      };
      HTTP.patch('', payload).then((response) => {
        this.project = response.data;
      });
    }, 300),
  },

});
