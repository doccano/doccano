import Vue from 'vue';
Vue.use(require('vue-shortkey'), { prevent: ['input', 'textarea'] });
import annotationMixin from './mixin.js';
import HTTP from './http.js';

Vue.component('annotator', {
    template: '<div @click="setSelectedRange">\
                   <span v-for="r in chunks" v-bind:class="{tag: r.color}" v-bind:style="{ color: r.color, backgroundColor: r.background }">{{ r.word }}<button v-if="r.color" class="delete is-small" @click="deleteLabel(r.index)"></button></span>\
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
        getBackgroundColor: function (label_id) {
            for (var item of this.labels) {
                if (item.id == label_id) {
                    return item.background_color
                }
            }
        },
        getTextColor: function (label_id) {
            for (var item of this.labels) {
                if (item.id == label_id) {
                    return item.text_color
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
            var i = 0;
            for (let i in this.sortedEntityPositions) {
                var e = this.sortedEntityPositions[i];
                var text = this.text.slice(left, e['start_offset']);
                res.push({
                    'word': text,
                    'color': '',
                    'background': ''
                });
                var text = this.text.slice(e['start_offset'], e['end_offset']);
                res.push({
                    'word': text,
                    'color': this.getTextColor(e.label.id),
                    'background': this.getBackgroundColor(e.label.id),
                    'index': i
                });
                left = e['end_offset'];
            }
            var text = this.text.slice(left, this.text.length);
            res.push({
                'word': text,
                'color': '',
                'background': ''
            });
            console.log(res);
            console.log(this.labels);
            console.log(this.entityPositions);

            return res
        }
    }
})

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    mixins: [annotationMixin],
    methods: {
        annotate: function (label_id) {
            var payload = this.$refs.annotator.addLabel(label_id);
            var doc_id = this.items[this.cur].id;
            HTTP.post(`docs/${doc_id}/annotations/`, payload).then(response => {
                this.items[this.cur]['labels'].push(response.data);
            });
            this.updateProgress()
        }
    }
});