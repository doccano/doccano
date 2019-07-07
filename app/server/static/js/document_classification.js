import Vue from 'vue';
import annotationMixin from './mixin';
import HTTP from './http';
import simpleShortcut from './filter';

import { toPercent, parseDate } from './filters'

Vue.filter('toPercent', toPercent)
Vue.filter('parseDate', parseDate)

import vueshortkey from './vue-shortkey'

Vue.use(vueshortkey, {
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

    async addLabel(label) {
      const a = this.isIn(label);
      let pageNumber = this.pageNumber
      this.labelKeyPress = false
      if (this.preventLabeling) {
        this.preventLabeling = false
        return
      }
      if (a) {
        this.removeLabel(a);
      } else {
        const docId = this.docs[pageNumber].id;
        const payload = {
          label: label.id,
        };
        await HTTP.post(`docs/${docId}/annotations/`, payload).then((response) => {
          this.annotations[pageNumber].push(response.data);
        });
      }
    },

    labelKeyDown() {
      if (!this.labelKeyPress) {
        this.labelKeyPress = true
      }
    }
  },
});
