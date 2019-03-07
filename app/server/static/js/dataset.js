import Vue from 'vue';

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    messages: []
  },
});
