import Vue from 'vue';
import annotationMixin from './mixin';
import HTTP from './http';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mixins: [annotationMixin],

  methods: {
    isIn(label) {
      for (let i = 0; i < this.annotations[this.cur].length; i++) {
        const a = this.annotations[this.cur][i];
        if (a.label === label.id) {
          return a;
        }
      }
      return false;
    },

    async addLabel(label) {
      const a = this.isIn(label);
      if (a) {
        this.removeLabel(a);
      } else {
        const docId = this.items[this.cur].id;
        const payload = {
          label: label.id,
        };
        await HTTP.post(`docs/${docId}/annotations/`, payload).then((response) => {
          this.annotations[this.cur].push(response.data);
        });
      }
    },
  },
});