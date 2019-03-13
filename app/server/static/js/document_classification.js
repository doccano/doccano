import Vue from 'vue';
import annotationMixin from './mixin';
import HTTP from './http';
import simpleShortcut from './filter';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

Vue.filter('simpleShortcut', simpleShortcut);


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mixins: [annotationMixin],

  methods: {
    isIn(label) {
      for (let i = 0; i < this.annotations[this.pageNumber].length; i++) {
        const a = this.annotations[this.pageNumber][i];
        if (a.label === label.id) {
          return a;
        }
      }
      return false;
    },

    async submit() {
      const state = this.getState();
      this.url = `docs?q=${this.searchQuery}&doc_annotations__isnull=${state}&offset=${this.offset}`;
      await this.search();
      this.pageNumber = 0;
    },

    async addLabel(label) {
      const a = this.isIn(label);
      if (a) {
        this.removeLabel(a);
      } else {
        const docId = this.docs[this.pageNumber].id;
        const payload = {
          label: label.id,
        };
        await HTTP.post(`docs/${docId}/annotations`, payload).then((response) => {
          this.annotations[this.pageNumber].push(response.data);
        });
      }
    },
  },
});
