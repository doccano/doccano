import Vue from 'vue';
import HTTP from './http';


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    labels: [],
    labelText: '',
    selectedShortkey: '',
    backgroundColor: '#209cee',
    textColor: '#ffffff',
  },

  methods: {
    addLabel() {
      const payload = {
        text: this.labelText,
        shortcut: this.selectedShortkey,
        background_color: this.backgroundColor,
        text_color: this.textColor,
      };
      HTTP.post('labels/', payload).then((response) => {
        this.reset();
        this.labels.push(response.data);
      });
    },

    removeLabel(label) {
      const labelId = label.id;
      HTTP.delete(`labels/${labelId}`).then((response) => {
        const index = this.labels.indexOf(label);
        this.labels.splice(index, 1);
      });
    },

    reset() {
      this.labelText = '';
      this.selectedShortkey = '';
      this.backgroundColor = '#209cee';
      this.textColor = '#ffffff';
    },
  },
  created() {
    HTTP.get('labels').then((response) => {
      this.labels = response.data;
    });
  },
});
