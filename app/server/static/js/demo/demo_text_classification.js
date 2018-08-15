import Vue from 'vue';
import annotationMixin from './demo_mixin';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mixins: [annotationMixin],
  data: {
    docs: [{
      id: 1,
      text: 'This is a document for named entity recognition.',
    },
    {
      id: 10,
      text: 'This is a sentence.',
    },
    {
      id: 11,
      text: 'This is a sentence.',
    },
    {
      id: 12,
      text: 'This is a sentence.',
    },
    {
      id: 13,
      text: 'This is a sentence.',
    },
    {
      id: 13,
      text: 'This is a sentence.',
    },
    ],
    labels: [
      {
        id: 1,
        text: 'Negative',
        shortcut: 'n',
        background_color: '#ff0033',
        text_color: '#ffffff',
      },
      {
        id: 2,
        text: 'Positive',
        shortcut: 'p',
        background_color: '#209cee',
        text_color: '#ffffff',
      },
    ],
    annotations: [
      [
        {
          id: 1,
          label: 1,
        },
      ],
      [],
      [],
      [],
      [],
      [],
    ],
  },

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

    addLabel(label) {
      const a = this.isIn(label);
      if (a) {
        this.removeLabel(a);
      } else {
        const annotation = {
          id: this.annotationId++,
          label: label.id,
        };
        this.annotations[this.pageNumber].push(annotation);
        console.log(this.annotations);
      }
    },
  },
});
