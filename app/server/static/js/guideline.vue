<template lang="pug">
  div.columns.is-gapless#editor(v-cloak="")
    div.column.is-6
      textarea.editorMarkdown_textarea(v-bind:value="input", v-debounce="update")
    div.column.is-6.has-background-white
      div.content.pt20.pb20.pr20.pl20
        div(v-html="compiledMarkdown")
</template>

<style scoped>
.column.is-6.has-background-white {
  border-right: 1px solid #dbdbdb;
  border-top: 1px solid #dbdbdb;
  border-bottom: 1px solid #dbdbdb;
}

.content {
  line-height: 150%;
}
</style>

<script>
import * as marked from 'marked';
import HTTP from './http';

export default {
  data: () => ({
    input: '',
    project: Object,
  }),

  computed: {
    compiledMarkdown() {
      return marked(this.input, {
        sanitize: true,
      });
    },
  },

  created() {
    HTTP.get().then((response) => {
      this.input = response.data.guideline;
      this.project = response.data;
    });
  },

  methods: {
    update(value) {
      this.input = value;
      const payload = {
        guideline: this.input,
      };
      HTTP.patch('', payload).then((response) => {
        this.project = response.data;
      });
    },
  },
};
</script>
