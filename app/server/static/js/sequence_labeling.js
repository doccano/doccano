import Vue from 'vue';
import annotationMixin from './mixin';
import HTTP from './http';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

Vue.component('annotator', {
  template: '<div @click="setSelectedRange">\
                    <span v-for="r in chunks"\
                         v-if="id2label[r.label]"\
                         v-bind:class="{tag: id2label[r.label].text_color}"\
                         v-bind:style="{ color: id2label[r.label].text_color, backgroundColor: id2label[r.label].background_color }"\
                    >{{ text.slice(r.start_offset, r.end_offset) }}<button class="delete is-small"\
                                         v-if="id2label[r.label].text_color"\
                                         @click="removeLabel(r)"></button></span>\
               </div>',
  props: {
    labels: Array, // [{id: Integer, color: String, text: String}]
    text: String,
    entityPositions: Array, // [{'startOffset': 10, 'endOffset': 15, 'label_id': 1}]
  },
  data() {
    return {
      startOffset: 0,
      endOffset: 0,
    };
  },

  methods: {
    setSelectedRange(e) {
      let start;
      let end;
      if (window.getSelection) {
        const range = window.getSelection().getRangeAt(0);
        const preSelectionRange = range.cloneRange();
        preSelectionRange.selectNodeContents(this.$el);
        preSelectionRange.setEnd(range.startContainer, range.startOffset);
        start = preSelectionRange.toString().length;
        end = start + range.toString().length;
      } else if (document.selection && document.selection.type !== 'Control') {
        const selectedTextRange = document.selection.createRange();
        const preSelectionTextRange = document.body.createTextRange();
        preSelectionTextRange.moveToElementText(this.$el);
        preSelectionTextRange.setEndPoint('EndToStart', selectedTextRange);
        start = preSelectionTextRange.text.length;
        end = start + selectedTextRange.text.length;
      }
      this.startOffset = start;
      this.endOffset = end;
      console.log(start, end);
    },

    validRange() {
      if (this.startOffset === this.endOffset) {
        return false;
      }
      if (this.startOffset > this.text.length || this.endOffset > this.text.length) {
        return false;
      }
      if (this.startOffset < 0 || this.endOffset < 0) {
        return false;
      }
      for (let i = 0; i < this.entityPositions.length; i++) {
        const e = this.entityPositions[i];
        if ((e.start_offset <= this.startOffset) && (this.startOffset < e.end_offset)) {
          return false;
        }
        if ((e.start_offset < this.endOffset) && (this.endOffset < e.end_offset)) {
          return false;
        }
        if ((this.startOffset < e.start_offset) && (e.start_offset < this.endOffset)) {
          return false;
        }
        if ((this.startOffset < e.end_offset) && (e.end_offset < this.endOffset)) {
          return false;
        }
      }
      return true;
    },

    resetRange() {
      this.startOffset = 0;
      this.endOffset = 0;
    },

    addLabel(labelId) {
      if (this.validRange()) {
        const label = {
          start_offset: this.startOffset,
          end_offset: this.endOffset,
          label: labelId,
        };
        this.$emit('add-label', label);
      }
    },

    removeLabel(index) {
      this.$emit('remove-label', index);
    },

    makeLabel(startOffset, endOffset) {
      const label = {
        id: 0,
        label: -1,
        start_offset: startOffset,
        end_offset: endOffset,
      };
      return label;
    },
  },

  watch: {
    entityPositions() {
      this.resetRange();
    },
  },

  computed: {
    sortedEntityPositions() {
      this.entityPositions = this.entityPositions.sort((a, b) => a.start_offset - b.start_offset);
      return this.entityPositions;
    },

    chunks() {
      const res = [];
      let left = 0;
      for (let i = 0; i < this.sortedEntityPositions.length; i++) {
        const e = this.sortedEntityPositions[i];
        const l = this.makeLabel(left, e.start_offset);
        res.push(l);
        res.push(e);
        left = e.end_offset;
      }
      const l = this.makeLabel(left, this.text.length);
      res.push(l);

      return res;
    },

    id2label() {
      let id2label = {};
      // default value;
      id2label[-1] = {
        text_color: '',
        background_color: '',
      };
      for (let i = 0; i < this.labels.length; i++) {
        const label = this.labels[i];
        id2label[label.id] = label;
      }
      return id2label;
    },
  },
});

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mixins: [annotationMixin],
  methods: {
    annotate(labelId) {
      this.$refs.annotator.addLabel(labelId);
    },

    addLabel(annotation) {
      const docId = this.docs[this.pageNumber].id;
      HTTP.post(`docs/${docId}/annotations/`, annotation).then((response) => {
        this.annotations[this.pageNumber].push(response.data);
      });
    },
  },
});
