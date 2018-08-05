axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
var base_url = window.location.href.split('/').slice(3, 5).join('/');
const HTTP = axios.create({
    baseURL: `/api/${base_url}/`,
})

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    data: {
        labels: [],
        labelText: '',
        selectedShortkey: '',
        backgroundColor: '#209cee',
        textColor: '#ffffff',
    },

    methods: {
        addLabel: function () {
            var payload = {
                text: this.labelText,
                shortcut: this.selectedShortkey,
                background_color: this.backgroundColor,
                text_color: this.textColor
            };
            HTTP.post('labels/', payload).then(response => {
                this.reset();
                this.labels.push(response.data);
            })
        },
        removeLabel: function (label) {
            var label_id = label.id;
            HTTP.delete(`labels/${label_id}`).then(response => {
                var index = this.labels.indexOf(label)
                this.labels.splice(index, 1)
            })
        },
        reset: function () {
            this.labelText = '';
            this.selectedShortkey = '';
            this.backgroundColor = '#209cee';
            this.textColor = '#ffffff';
        }
    },
    created: function () {
        HTTP.get('labels').then(response => {
            this.labels = response.data
        })
    }
})