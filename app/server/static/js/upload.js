import Vue from 'vue';


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    file: '',
  },

  methods: {
    handleFileUpload() {
      console.log(this.$refs.file.files);
      this.file = this.$refs.file.files[0].name;
    },
  },
});
