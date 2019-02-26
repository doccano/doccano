/* eslint-disable no-new */

import Vue from 'vue';

new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    file: '',
    uploadFormat: 'json',
    updateExisting: false,
    importAnnotations: false,
  },

  methods: {
    handleFileUpload() {
      console.log(this.$refs.file.files);
      this.file = this.$refs.file.files[0].name;
    },
    uncheckAnnotationImport() {
      this.importAnnotations = false;
    },
  },
});
