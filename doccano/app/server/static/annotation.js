import Vue from 'vue';
Vue.use(require('vue-shortkey'));

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
var base_url = window.location.href.split('/').slice(3, 5).join('/');
const HTTP = axios.create({
    baseURL: `/api/${base_url}/`
})

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    data: {
        cur: 0,
        items: [{id: null, text: '', labels: []}],
        labels: [],
        guideline: 'Here is the Annotation Guideline Text',
        total: 0,
        remaining: 0,
        searchQuery: '',
        url: '',
    },

    methods: {
        addLabel: async function (label_id) {
            for (var i = 0; i < this.items[this.cur]['labels'].length; i++) {
                var item = this.items[this.cur]['labels'][i];
                if (label_id == item.label.id) {
                    this.deleteLabel(i);
                    return;
                }
            }

            var payload = {
                'label_id': label_id
            };

            var doc_id = this.items[this.cur].id;
            await HTTP.post(`docs/${doc_id}/annotations/`, payload).then(response => {
                this.items[this.cur]['labels'].push(response.data);
            });
            this.updateProgress();
        },
        deleteLabel: async function (index) {
            var doc_id = this.items[this.cur].id;
            var annotation_id = this.items[this.cur]['labels'][index].id;
            HTTP.delete(`docs/${doc_id}/annotations/${annotation_id}`).then(response => {
                this.items[this.cur]['labels'].splice(index, 1)
            });
            this.updateProgress();
        },
        nextPage: async function () {
            this.cur += 1;
            if (this.cur == this.items.length) {
                if (this.next) {
                    this.url = this.next;
                    await this.search();
                    this.cur = 0;
                } else {
                    this.cur = this.items.length - 1;
                }
            }
            this.showMessage(this.cur);
        },
        prevPage: async function () {
            this.cur -= 1;
            if (this.cur == -1) {
                if (this.prev) {
                    this.url = this.prev;
                    await this.search();
                    this.cur = this.items.length - 1;
                } else {
                    this.cur = 0;
                }
            }
            this.showMessage(this.cur);
        },
        submit: function () {
            this.url = `docs/?q=${this.searchQuery}`;
            this.search();
        },
        search: async function () {
            await HTTP.get(this.url).then(response => {
                this.items = response.data['results'];
                this.next = response.data['next'];
                this.prev = response.data['previous'];
            })
        },
        showMessage: function (index) {
            this.cur = index;
        },
        updateProgress: function () {
            HTTP.get('progress').then(response => {
                this.total = response.data['total'];
                this.remaining = response.data['remaining'];
            })
        }
    },
    created: function () {
        HTTP.get('labels').then(response => {
            this.labels = response.data
        });
        this.updateProgress();
        this.submit();
    },
    computed: {
        achievement: function () {
            var done = this.total - this.remaining;
            var percentage = Math.round(done / this.total * 100);
            return this.total > 0 ? percentage : 0;
        },
        progressColor: function () {
            if (this.achievement < 30) {
                return 'is-danger'
            } else if (this.achievement < 70) {
                return 'is-warning'
            } else {
                return 'is-primary'
            }
        }
    }
});