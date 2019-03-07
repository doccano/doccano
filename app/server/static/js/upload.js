import Vue from 'vue';
import HTTP from './http';

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    file: '',
    messages: [],
    format: 'json',
  },

  methods: {

    upload() {
      this.file = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append('file', this.file);
      formData.append('format', this.format);
      HTTP.post('docs/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          console.log(response);
          this.messages = [];
        })
        .catch((error) => {
          if ('detail' in error.response.data) {
            this.messages.push(error.response.data.detail);
          } else if ('text' in error.response.data) {
            this.messages = error.response.data.text;
          }
        });
    },

    download() {
      HTTP({
        url: 'docs/download',
        method: 'GET',
        responseType: 'blob',
        params: {
          q: this.format,
        },
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'file.' + this.format); //or any other extension
        document.body.appendChild(link);
        link.click();
      }).catch((error) => {
        if ('detail' in error.response.data) {
          this.messages.push(error.response.data.detail);
        } else if ('text' in error.response.data) {
          this.messages = error.response.data.text;
        }
      });
    },
  },
});
