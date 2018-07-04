axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
var base_url = window.location.href.split('/').slice(3, 5).join('/');
const HTTP = axios.create({
    baseURL: `/api/${base_url}/`,
})

var vm = new Vue({
    el: '#root',
    delimiters: ['[[', ']]'],
    data: {
        labels: [],
        file: null,
        file_name: '',
        newLabel: '',
        newShortcut: '',
        total: 0,
        remaining: 0,
    },

    methods: {
        handleFileUpload() {
            this.file = this.$refs.file.files[0];
            this.file_name = this.file.name;
        },
        submitFile() {
            let formData = new FormData();
            formData.append('file', this.file);
            axios.post('/' + base_url + '/apis/raw_data',
                    formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                ).then(function () {
                    console.log('SUCCESS!!');
                })
                .catch(function () {
                    console.log('FAILURE!!');
                });
        },
        addLabel: function () {
            var payload = {
                text: this.newLabel,
                shortcut: this.newShortcut
            };
            HTTP.post('labels/', payload).then(response => {
                this.newLabel = '';
                this.newShortcut = '';
                this.labels.push(response.data);
            })
        },
        removeLabel: function (index) {
            var label_id = this.labels[index].id;
            HTTP.delete(`labels/${label_id}`).then(response => {
                this.labels.splice(index, 1)
            })
        }
    },
    created: function () {
        HTTP.get('labels').then(response => {
            this.labels = response.data
        })
        HTTP.get('progress').then(response => {
            this.total = response.data['total'];
            this.remaining = response.data['remaining'];
        })
    }
})