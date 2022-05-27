<template>
  <file-pond
    ref="pond"
    chunk-uploads="true"
    label-idle="Drop files here..."
    :allow-multiple="false"
    :server="server"
    :files="myFiles"
    @processfile="handleFilePondProcessfile"
    @removefile="handleFilePondRemovefile"
  />
</template>

<script>
import Cookies from 'js-cookie'
import vueFilePond from 'vue-filepond'
import 'filepond/dist/filepond.min.css'
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type'
const FilePond = vueFilePond(FilePondPluginFileValidateType)

export default {
  components: {
    FilePond
  },

  props: {
    value: {
      type: String,
      default: '',
      required: true
    }
  },

  data() {
    return {
      myFiles: [],
      server: {
        url: '/v1/fp',
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        process: {
          url: '/process/',
          method: 'POST'
        },
        patch: '/patch/',
        revert: '/revert/',
        restore: '/restore/',
        load: '/load/',
        fetch: '/fetch/'
      }
    }
  },

  methods: {
    handleFilePondProcessfile(error, file) {
      console.log(error)
      this.$emit('input', file.serverId)
    },
    handleFilePondRemovefile() {
      this.$emit('input', '')
    }
  }
}
</script>
