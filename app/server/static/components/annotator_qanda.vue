<template lang="pug">
  div(@click="setSelectedRange")
    span.text-sequence(
      v-for="r in chunks"
      v-bind:class="getChunkClass(r)"
      v-bind:style="getChunkStyle(r)"
    ) {{ textPart(r) }}
      button.delete.is-small(v-if="r.label==1", v-on:click="removeAnswer(r)")
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: '',
    },
    entityPositions: {
      type: Array, // [{'startOffset': 10, 'endOffset': 15, 'label_id': 1}]
      default: () => [],
    },
  },

  data: () => ({
    startOffset: 0,
    endOffset: 0,
  }),

  computed: {
    sortedEntityPositions() {
      /* eslint-disable vue/no-side-effects-in-computed-properties */
      return this.entityPositions.sort((a, b) => a.start_offset - b.start_offset);
      /* eslint-enable vue/no-side-effects-in-computed-properties */
    },

    chunks() {
      const res = [];
      let left = 0;
      for (let entity of this.sortedEntityPositions) {
        entity.label = 1;
        entity.end_offset = entity.start_offset + entity.response.length;

        const emptyChunk = this.makeEmptyChunk(left, entity.start_offset);
        res.push(emptyChunk);
        res.push(entity);
        left = entity.end_offset;
      }
      const emptyChunk = this.makeEmptyChunk(left, this.text.length);
      res.push(emptyChunk);
      console.log(res);
      return res;
    },

  },

  watch: {
    entityPositions() {
      this.resetRange();
    },
  },

  methods: {
    getChunkClass(chunk) {
      if (chunk.label === 0) {
        return {};
      }
      return [
        { tag: '#ffffff' },
      ];
    },

    getChunkStyle(chunk) {
      if (chunk.label === 0) {
        return {};
      }
      return {
        color: '#ffffff',
        backgroundColor: '#4169e1',
      };
    },


    setSelectedRange() {
      let start;
      let end;
      if (window.getSelection) {
        const range = window.getSelection().getRangeAt(0);
        const preSelectionRange = range.cloneRange();
        preSelectionRange.selectNodeContents(this.$el);
        preSelectionRange.setEnd(range.startContainer, range.startOffset);
        start = [...preSelectionRange.toString()].length;
        end = start + [...range.toString()].length;
      } else if (document.selection && document.selection.type !== 'Control') {
        const selectedTextRange = document.selection.createRange();
        const preSelectionTextRange = document.body.createTextRange();
        preSelectionTextRange.moveToElementText(this.$el);
        preSelectionTextRange.setEndPoint('EndToStart', selectedTextRange);
        start = [...preSelectionTextRange.text].length;
        end = start + [...selectedTextRange.text].length;
      }
      this.startOffset = start;
      this.endOffset = end;
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
      for (let e of this.entityPositions) {
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

    hasAnswer() {
      if (this.entityPositions.length > 0) {
        return true;
      }
      return false;
    },

    resetRange() {
      this.startOffset = 0;
      this.endOffset = 0;
    },

    textPart(r) {
      return [...this.text].slice(r.start_offset, r.end_offset).join('');
    },

    addAnswer() {
      if (this.validRange() && !this.hasAnswer()) {
        const text = {
          start_offset: this.startOffset,
          response: [...this.text].slice(this.startOffset, this.endOffset).join(''),
        };
        this.$emit('add-answer', text);
      }
    },

    removeAnswer(index) {
      this.$emit('remove-answer', index);
    },

    makeEmptyChunk(startOffset, endOffset) {
      const chunk = {
        id: 0,
        label: 0,
        start_offset: startOffset,
        end_offset: endOffset,
      };
      return chunk;
    },
  },
};
</script>
