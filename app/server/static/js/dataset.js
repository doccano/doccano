import Vue from 'vue';

const vm = new Vue({ // eslint-disable-line no-unused-vars
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    messages: [],
  },
});
