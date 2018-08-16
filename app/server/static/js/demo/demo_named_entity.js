import Vue from 'vue';
import annotationMixin from './demo_mixin';

Vue.use(require('vue-shortkey'), {
  prevent: ['input', 'textarea'],
});

Vue.component('annotator', {
  template: '<div @click="setSelectedRange">\
                    <span v-for="r in chunks"\
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
        if ((e.start_offset <= this.startOffset) && (this.startOffset <= e.end_offset)) {
          return false;
        }
        if ((e.start_offset <= this.endOffset) && (this.endOffset <= e.end_offset)) {
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
  data: {
    docs: [{
      id: 1,
      text: 'Barack Hussein Obama II (born August 4, 1961) is an American attorney and politician who served as the 44th President of the United States from January 20, 2009, to January 20, 2017. A member of the Democratic Party, he was the first African American to serve as president. He was previously a United States Senator from Illinois and a member of the Illinois State Senate.',
    },
    {
      id: 10,
      text: 'The White House is the official residence and workplace of the President of the United States. It is located at 1600 Pennsylvania Avenue NW in Washington, D.C. and has been the residence of every U.S. President since John Adams in 1800. The term is often used as a metonym for the president and his advisers.',
    },
    {
      id: 11,
      text: "The Democratic Party is one of the two major contemporary political parties in the United States, along with the Republican Party. Tracing its heritage back to Thomas Jefferson and James Madison's Democratic-Republican Party, the modern-day Democratic Party was founded around 1828 by supporters of Andrew Jackson, making it the world's oldest active political party.",
    },
    {
      id: 12,
      text: "Stanford University (officially Leland Stanford Junior University, colloquially the Farm) is a private research university in Stanford, California. Stanford is known for its academic strength, wealth, proximity to Silicon Valley, and ranking as one of the world's top universities.",
    },
    {
      id: 13,
      text: 'Donald John Trump (born June 14, 1946) is the 45th and current President of the United States. Before entering politics, he was a businessman and television personality.',
    },
    {
      id: 14,
      text: "Silicon Valley (abbreviated as SV) is a region in the southern San Francisco Bay Area of Northern California, referring to the Santa Clara Valley, which serves as the global center for high technology, venture capital, innovation, and social media. San Jose is the Valley's largest city, the 3rd-largest in California, and the 10th-largest in the United States. Other major SV cities include Palo Alto, Santa Clara, Mountain View, and Sunnyvale. The San Jose Metropolitan Area has the third highest GDP per capita in the world (after Zurich, Switzerland and Oslo, Norway), according to the Brookings Institution.",
    },
    ],
    labels: [
      {
        id: 1,
        text: 'Person',
        shortcut: 'p',
        background_color: '#209cee',
        text_color: '#ffffff',
      },
      {
        id: 2,
        text: 'Loc',
        shortcut: 'l',
        background_color: '#ffcc00',
        text_color: '#333333',
      },
      {
        id: 3,
        text: 'Org',
        shortcut: 'o',
        background_color: '#333333',
        text_color: '#ffffff',
      },
      {
        id: 4,
        text: 'Event',
        shortcut: 'e',
        background_color: '#33cc99',
        text_color: '#ffffff',
      },
      {
        id: 5,
        text: 'Date',
        shortcut: 'd',
        background_color: '#ff3333',
        text_color: '#ffffff',
      },
      {
        id: 6,
        text: 'Other',
        shortcut: 'z',
        background_color: '#9933ff',
        text_color: '#ffffff',
      },
    ],
    annotations: [
      [
        {
          id: 16,
          prob: 0.0,
          label: 1,
          start_offset: 0,
          end_offset: 23,
        },
        {
          id: 19,
          prob: 0.0,
          label: 2,
          start_offset: 121,
          end_offset: 138,
        },
        {
          id: 27,
          prob: 0.0,
          label: 2,
          start_offset: 321,
          end_offset: 329,
        },
        {
          id: 22,
          prob: 0.0,
          label: 3,
          start_offset: 199,
          end_offset: 215,
        },
        {
          id: 28,
          prob: 0.0,
          label: 3,
          start_offset: 350,
          end_offset: 371,
        },
        {
          id: 17,
          prob: 0.0,
          label: 5,
          start_offset: 30,
          end_offset: 44,
        },
        {
          id: 20,
          prob: 0.0,
          label: 5,
          start_offset: 144,
          end_offset: 160,
        },
        {
          id: 21,
          prob: 0.0,
          label: 5,
          start_offset: 165,
          end_offset: 181,
        },
        {
          id: 18,
          prob: 0.0,
          label: 6,
          start_offset: 52,
          end_offset: 60,
        },
        {
          id: 24,
          prob: 0.0,
          label: 6,
          start_offset: 234,
          end_offset: 250,
        },
        {
          id: 26,
          prob: 0.0,
          label: 6,
          start_offset: 294,
          end_offset: 315,
        },
      ],
      [],
      [],
      [],
      [],
      [],
    ],
  },

  methods: {
    annotate(labelId) {
      this.$refs.annotator.addLabel(labelId);
    },

    addLabel(annotation) {
      this.annotations[this.pageNumber].push(annotation);
    },
  },
});
