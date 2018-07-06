//import Vue from 'vue';
//Vue.use(require('vue-shortkey'));

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
var base_url = window.location.href.split('/').slice(3, 5).join('/');
const HTTP = axios.create({
    baseURL: `/api/${base_url}/`
})

const Annotator = {
    template: '<div @click="setSelectedRange">\
                   <span v-for="r in chunks" :class="r.color">{{ r.word }}<button v-if="r.color" class="delete is-small" @click="deleteLabel(r.index)"></button></span>\
               </div>',
    props: {
        'labels': Array, // [{id: Integer, color: String, text: String}]
        'text': String,
        'entityPositions': Array, //[{'startOffset': 10, 'endOffset': 15, 'label_id': 1}]
    },
    data() {
        return {
            startOffset: 0,
            endOffset: 0,
        }
    },
    methods: {
        setSelectedRange: function (e) {
            if (window.getSelection) {
                var range = window.getSelection().getRangeAt(0);
                var preSelectionRange = range.cloneRange();
                preSelectionRange.selectNodeContents(this.$el);
                preSelectionRange.setEnd(range.startContainer, range.startOffset);
                var start = preSelectionRange.toString().length;
                var end = start + range.toString().length;
            } else if (document.selection && document.selection.type != 'Control') {
                var selectedTextRange = document.selection.createRange();
                var preSelectionTextRange = document.body.createTextRange();
                preSelectionTextRange.moveToElementText(this.$el);
                preSelectionTextRange.setEndPoint('EndToStart', selectedTextRange);
                var start = preSelectionTextRange.text.length;
                var end = start + selectedTextRange.text.length;
            }
            this.startOffset = start;
            this.endOffset = end;
            console.log(start, end);
        },
        validRange: function () {
            if (this.startOffset == this.endOffset) {
                return false
            } else if (this.startOffset > this.text.length || this.endOffset > this.text.length) {
                return false
            } else if (this.startOffset < 0 || this.endOffset < 0) {
                return false
            } else {
                return true
            }
        },
        resetRange: function () {
            this.startOffset = 0;
            this.endOffset = 0
        },
        addLabel: function (label_id) {
            if (this.validRange()) {
                var label = {
                    start_offset: this.startOffset,
                    end_offset: this.endOffset,
                    label_id: label_id
                };
                this.entityPositions.push(label);
                return label
            }
        },
        deleteLabel: function (index) {
            this.$emit('delete-label', index);
            this.entityPositions.splice(index, 1)
        },
        getColor: function (label_id) {
            for (item of this.labels) {
                if (item.id == label_id) {
                    return item.color
                }
            }
        }
    },
    watch: {
        entityPositions: function () {
            this.resetRange()
        }
    },
    computed: {
        sortedEntityPositions: function () {
            return this.entityPositions.sort((a, b) => a.start_offset - b.start_offset)
        },
        chunks: function () {
            var res = [];
            var left = 0;
            for (let [i, e] of this.sortedEntityPositions.entries()) {
                var text = this.text.slice(left, e['start_offset']);
                res.push({
                    'word': text,
                    'color': ''
                });
                var text = this.text.slice(e['start_offset'], e['end_offset']);
                res.push({
                    'word': text,
                    'color': 'tag is-info',//this.getColor(e['label_id']),
                    'index': i
                });
                left = e['end_offset'];
            }
            var text = this.text.slice(left, this.text.length);
            res.push({
                'word': text,
                'color': ''
            });

            return res
        }
    }
}

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    components: {
        'annotator': Annotator,
    },
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
        annotate: function (label_id) {
            var payload = this.$refs.annotator.addLabel(label_id);
            var doc_id = this.items[this.cur].id;
            HTTP.post(`docs/${doc_id}/annotations/`, payload).then(response => {
                this.items[this.cur]['labels'].push(response.data);
            });
            this.updateProgress()
        },
        addLabel: function (label_id) {
            
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
        submit: async function () {
            this.url = `docs/?q=${this.searchQuery}`;
            await this.search();
            this.cur = 0;
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