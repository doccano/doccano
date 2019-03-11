import Vue from 'vue';
import HTTP from './http';

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    file: '',
    messages: [],
    format: 'json',
    isLoading: false,
  },

  methods: {

    upload() {
      this.isLoading = true;
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
          window.location = window.location.pathname.split('/').slice(0, -1).join('/');
        })
        .catch((error) => {
          this.isLoading = false;
          if ('detail' in error.response.data) {
            this.messages.push(error.response.data.detail);
          } else if ('text' in error.response.data) {
            this.messages = error.response.data.text;
          }
        });
    },

    download() {
      let headers = {};
      if (this.format === 'csv') {
        headers.Accept = 'text/csv; charset=utf-8';
        headers['Content-Type'] = 'text/csv; charset=utf-8';
      } else {
        headers.Accept = 'application/json';
        headers['Content-Type'] = 'application/json';
      }
      HTTP({
        url: 'docs/download',
        method: 'GET',
        responseType: 'blob',
        params: {
          q: this.format,
        },
        headers,
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
