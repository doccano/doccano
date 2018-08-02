import HTTP from './http.js';

var annotationMixin = {
    data: function () {
        return {
            cur: 0,
            items: [{
                id: null,
                text: '',
                labels: []
            }],
            labels: [],
            guideline: 'Here is the Annotation Guideline Text',
            total: 0,
            remaining: 0,
            searchQuery: '',
            url: '',
            picked: 'all',
        }
    },
    methods: {
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
        getState: function () {
            if (this.picked == 'all') {
                return ''
            } else if (this.picked == 'active') {
                return 'true'
            } else {
                return 'false'
            }
        },
        submit: async function () {
            var state = this.getState();
            this.url = `docs/?q=${this.searchQuery}&is_checked=${state}`;
            await this.search();
            this.cur = 0;
        },
        deleteLabel: async function (index) {
            var doc_id = this.items[this.cur].id;
            var annotation_id = this.items[this.cur]['labels'][index].id;
            HTTP.delete(`docs/${doc_id}/annotations/${annotation_id}`).then(response => {
                this.items[this.cur]['labels'].splice(index, 1)
            })
        },

        removeLabel: function (label) {
            var doc_id = this.items[this.cur].id;
            HTTP.delete(`docs/${doc_id}/annotations/${label.id}`).then(response => {
                var index = this.items[this.cur]['labels'].indexOf(label)
                this.items[this.cur]['labels'].splice(index, 1)
            })
        }
    },
    watch: {
        picked: function (){
            this.submit();
        },
        items: function () {
            // fetch progress info.
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
};

export default annotationMixin;