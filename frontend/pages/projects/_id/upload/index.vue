<template>
  <file-pond
    ref="pond"
    label-idle="Drop files here..."
    :allow-multiple="true"
    :server="server"
    :files="myFiles"
    @init="handleFilePondInit"
  />
</template>

<script>
import Cookies from 'js-cookie'
import vueFilePond from "vue-filepond"
import "filepond/dist/filepond.min.css"
const FilePond = vueFilePond()

export default {
  layout: 'project',

  components: {
    FilePond,
  },
  
  data() {
    return {
      myFiles: [],
      server: {
        url: '/v1/fp',
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken'),
        },
        process: '/process/',
        revert: '/revert/',
        restore: '/restore/',
        load: '/load/',
        fetch: '/fetch/'
      }
    }
  },

  methods: {
    handleFilePondInit() {
      console.log("FilePond has initialized");
    },
  },
};
</script>
