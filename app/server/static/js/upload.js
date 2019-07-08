import Vue from 'vue';


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    file: '',
    urlMode: false,
    activeTab: 1,
    selectedFormat: 'csv',
    inputUrl: '',
    formats: {
      local: [
        {
          value: 'csv',
          text: 'Upload a CSV file from your computer'
        },
        {
          value: 'json',
          text: 'Upload a JSON file from your computer'
        },
        {
          value: 'csv_labeled',
          text: 'Upload a labeled CSV file from your computer'
        },
        {
          value: 'csv_labeled_users',
          text: 'Upload a users labeled CSV file from your computer'
        }
      ],
      url: [
        {
          value: 'csv_url',
          text: 'Upload a CSV file from URL'
        },
        {
          value: 'json_url',
          text: 'Upload a JSON file from URL'
        },
        {
          value: 'csv_labeled_url',
          text: 'Upload a labeled CSV file from URL'
        },
        {
          value: 'csv_labeled_users_url',
          text: 'Upload a users labeled CSV file from URL'
        }
      ]
    }
  },

  methods: {
    handleFileUpload() {
      this.file = this.$refs.file.files[0].name;
    },
    submit(e) {
      if (!this.file && this.activeTab === 1) {
        e.preventDefault()
        return
      }

      if ((!this.inputUrl || !this.inputUrl.length) && this.activeTab === 2) {
        e.preventDefault()
        return
      }
    },
    setTab(tab) {
      this.activeTab = tab
      if (tab === 1) {
        this.selectedFormat = 'csv'
      } else {
        this.selectedFormat = 'csv_url'
      }
    }
  },
});
