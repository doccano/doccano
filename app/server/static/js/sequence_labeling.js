import Vue from 'vue';
Vue.use(require('vue-shortkey'), { prevent: ['input', 'textarea'] });
import annotationMixin from './mixin.js';
import HTTP from './http.js';

Vue.component('annotator', {
    template: '<div @click="setSelectedRange">\
                    <span v-for="r in chunks"\
                         v-bind:class="{tag: r.label.text_color}"\
                         v-bind:style="{ color: r.label.text_color, backgroundColor: r.label.background_color }"\
                    >{{ text.slice(r.start_offset, r.end_offset) }}<button class="delete is-small"\
                                         v-if="r.label.text_color"\
                                         @click="deleteLabel(r)"></button></span>\
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
                this.$emit('add-label', label);
            }
        },
        deleteLabel: function (index) {
            this.$emit('delete-label', index);
        },
        makeLabel: function (start_offset, end_offset) {
            var label = {
                id: 0,
                label: {
                    id: -1,
                    text: '',
                    shortcut: '',
                    background_color: '',
                    text_color: ''
                },
                start_offset: start_offset,
                end_offset: end_offset
            }
            return label
        }
    },
    watch: {
        entityPositions: function () {
            this.resetRange()
        }
    },
    computed: {
        sortedEntityPositions: function () {
            this.entityPositions = this.entityPositions.sort((a, b) => a.start_offset - b.start_offset);
            return this.entityPositions
        },
        chunks: function () {
            var res = [];
            var left = 0;
            for (let i in this.sortedEntityPositions) {
                var e = this.sortedEntityPositions[i];
                var l = this.makeLabel(left, e['start_offset'])
                res.push(l);
                res.push(e);
                left = e['end_offset'];
            }
            var l = this.makeLabel(left, this.text.length)
            res.push(l)

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
        },
        addLabel: function (label) {
            var payload = label;
            var doc_id = this.items[this.cur].id;
            payload['label'] = label.label_id;
            HTTP.post(`docs/${doc_id}/annotations/`, payload).then(response => {
                this.items[this.cur]['labels'].push(response.data);
            })
        },
        deleteLabel: function (label) {
            var doc_id = this.items[this.cur].id;
            HTTP.delete(`docs/${doc_id}/annotations/${label.id}`).then(response => {
                this.items[this.cur]['labels'].splice(this.items[this.cur]['labels'].indexOf(label), 1)
            });
        },
    }
});