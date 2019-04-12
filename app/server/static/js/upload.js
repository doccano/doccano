import Vue from 'vue';
import HTTP from './http';

const vm = new Vue({ // eslint-disable-line no-unused-vars
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
      const formData = new FormData();
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
          console.log(response); // eslint-disable-line no-console
          this.messages = [];
          window.location = window.location.pathname.split('/').slice(0, -1).join('/');
        })
        .catch((error) => {
          this.isLoading = false;
          this.handleError(error);
        });
    },

    handleError(error) {
      const problems = Array.isArray(error.response.data)
        ? error.response.data
        : [error.response.data];

      problems.forEach((problem) => {
        if ('detail' in problem) {
          this.messages.push(problem.detail);
        } else if ('text' in problem) {
          this.messages = problem.text;
        }
      });
    },

    download() {
      const headers = {};
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
        link.setAttribute('download', 'file.' + this.format); // or any other extension
        document.body.appendChild(link);
        link.click();
      }).catch((error) => {
        this.handleError(error);
      });
    },
  },
});
