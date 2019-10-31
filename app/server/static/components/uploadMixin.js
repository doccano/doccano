import hljs from 'highlight.js/lib/highlight';
import hljsLanguages from './hljsLanguages';
import HTTP, { defaultHttpClient } from './http';
import Messages from './messages.vue';

const sleep = ms => new Promise((resolve, _) => setTimeout(resolve, ms));

hljsLanguages.forEach((languageName) => {
  /* eslint-disable import/no-dynamic-require, global-require */
  const languageModule = require(`highlight.js/lib/languages/${languageName}`);
  /* eslint-enable import/no-dynamic-require, global-require */
  hljs.registerLanguage(languageName, languageModule);
});

export default {
  components: { Messages },

  data: () => ({
    file: '',
    messages: [],
    format: 'json',
    isLoading: false,
    isCloudUploadActive: false,
    canUploadFromCloud: false,
  }),

  mounted() {
    hljs.initHighlighting();
  },

  created() {
    defaultHttpClient.get('/v1/features').then((response) => {
      this.canUploadFromCloud = response.data.cloud_upload;
    });
  },

  computed: {
    projectId() {
      return window.location.pathname.split('/')[2];
    },

    postUploadUrl() {
      return window.location.pathname.split('/').slice(0, -1).join('/');
    },

    cloudUploadUrl() {
      return '/cloud-storage'
        + `?project_id=${this.projectId}`
        + `&upload_format=${this.format}`
        + `&next=${encodeURIComponent('about:blank')}`;
    },
  },

  methods: {
    cloudUpload() {
      const iframeUrl = this.$refs.cloudUploadPane.contentWindow.location.href;
      if (iframeUrl.indexOf('/v1/cloud-upload') > -1) {
        this.isCloudUploadActive = false;
        this.$nextTick(() => {
          window.location.href = this.postUploadUrl;
        });
      }
    },

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
          window.location = this.postUploadUrl;
        })
        .catch((error) => {
          this.isLoading = false;
          this.handleError(error);
        });
    },

    handleError(error) {
      let problems;
      if (error.response && error.response.data) {
        problems = Array.isArray(error.response.data)
          ? error.response.data
          : [error.response.data];
      } else if (error.message) {
        problems = [{ detail: error.message }];
      } else {
        console.error('Unrecognized error type', error); // eslint-disable-line no-console
        problems = [];
      }

      problems.forEach((problem) => {
        if ('detail' in problem) {
          this.messages.push(problem.detail);
        } else if ('text' in problem) {
          this.messages = problem.text;
        }
      });
    },

    async download() {
      this.isLoading = true;

      let taskResponse;
      try {
        taskResponse = await HTTP({
          url: 'docs/download',
          method: 'GET',
          params: {
            q: this.format,
          },
        });
      } catch (error) {
        this.isLoading = false;
        this.handleError(error);
        return;
      }

      const taskId = taskResponse.data.task_id;

      /* eslint-disable no-await-in-loop */
      while (this.isLoading) {
        let statusResponse;
        try {
          statusResponse = await defaultHttpClient.get(`/v1/tasks/status/${taskId}`);
        } catch (error) {
          this.isLoading = false;
          this.handleError(error);
          return;
        }

        if (statusResponse.data.error) {
          this.isLoading = false;
          this.handleError(new Error(statusResponse.data.error.text));
          return;
        }

        if (statusResponse.data.ready) {
          const url = window.URL.createObjectURL(new Blob([statusResponse.data.result]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', `file.${this.format}`);
          document.body.appendChild(link);
          this.isLoading = false;
          link.click();
        } else {
          await sleep(1000);
        }
      }
      /* eslint-enable no-await-in-loop */
    },
  },
};
