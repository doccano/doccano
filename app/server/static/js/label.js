import Vue from 'vue';
import HTTP from './http';
import { simpleShortcut } from './filter';

Vue.filter('simpleShortcut', simpleShortcut);


const vm = new Vue({ // eslint-disable-line no-unused-vars
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    labels: [],
    newLabel: null,
    editedLabel: null,
    messages: [],
  },

  methods: {
    generateColor() {
      const color = (Math.random() * 0xFFFFFF | 0).toString(16); // eslint-disable-line no-bitwise
      const randomColor = '#' + ('000000' + color).slice(-6);
      return randomColor;
    },

    blackOrWhite(hexcolor) {
      const r = parseInt(hexcolor.substr(1, 2), 16);
      const g = parseInt(hexcolor.substr(3, 2), 16);
      const b = parseInt(hexcolor.substr(5, 2), 16);
      return ((((r * 299) + (g * 587) + (b * 114)) / 1000) < 128) ? '#ffffff' : '#000000';
    },

    setColor(label) {
      const bgColor = this.generateColor();
      const textColor = this.blackOrWhite(bgColor);
      label.background_color = bgColor;
      label.text_color = textColor;
    },

    shortcutKey(label) {
      let shortcut = label.suffix_key;
      if (label.prefix_key) {
        shortcut = `${label.prefix_key} ${shortcut}`;
      }
      return shortcut;
    },

    sortLabels() {
      return this.labels.sort((a, b) => ((a.text < b.text) ? -1 : 1));
    },

    addLabel() {
      HTTP.post('labels', this.newLabel)
        .then((response) => {
          this.cancelCreate();
          this.labels.push(response.data);
          this.sortLabels();
          this.messages = [];
        })
        .catch((error) => {
          console.log(error); // eslint-disable-line no-console
          this.messages.push('You cannot use same label name or shortcut key.');
        });
    },

    removeLabel(label) {
      const labelId = label.id;
      HTTP.delete(`labels/${labelId}`).then(() => {
        const index = this.labels.indexOf(label);
        this.labels.splice(index, 1);
      });
    },

    createLabel() {
      this.newLabel = {
        text: '',
        prefix_key: null,
        suffix_key: null,
        background_color: '#209cee',
        text_color: '#ffffff',
      };
    },

    cancelCreate() {
      this.newLabel = null;
    },

    editLabel(label) {
      this.beforeEditCache = Object.assign({}, label);
      this.editedLabel = label;
    },

    doneEdit(label) {
      if (!this.editedLabel) {
        return;
      }
      this.editedLabel = null;
      label.text = label.text.trim();
      if (!label.text) {
        this.removeLabel(label);
      }
      HTTP.patch(`labels/${label.id}`, label)
        .then(() => {
          this.sortLabels();
          this.messages = [];
        })
        .catch((error) => {
          console.log(error); // eslint-disable-line no-console
          this.messages.push('You cannot use same label name or shortcut key.');
        });
    },

    cancelEdit(label) {
      this.editedLabel = null;
      Object.assign(label, this.beforeEditCache);
    },
  },
  created() {
    HTTP.get('labels').then((response) => {
      this.labels = response.data;
      this.sortLabels();
    });
  },
});
