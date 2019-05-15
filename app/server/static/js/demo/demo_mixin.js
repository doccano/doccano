import * as marked from 'marked';

const annotationMixin = {
  data() {
    return {
      pageNumber: 0,
      docs: [],
      annotations: [],
      labels: [],
      tmp_docs: [],
      tmp_annotations: [],
      guideline: 'You can see annotation guideline here.',
      searchQuery: '',
      picked: 'all',
      annotationId: 100,
      isMetadataActive: false,
      isAnnotationGuidelineActive: false,
    };
  },

  methods: {
    nextPage() {
      this.pageNumber = Math.min(this.pageNumber + 1, this.docs.length - 1);
    },

    prevPage() {
      this.pageNumber = Math.max(this.pageNumber - 1, 0);
    },

    search() {
      this.docs = [];
      this.annotations = [];
      for (let i = 0; i < this.tmp_docs.length; i++) {
        if (this.tmp_docs[i].text.indexOf(this.searchQuery) !== -1) {
          if (this.picked === 'all') {
            this.docs.push(this.tmp_docs[i]);
            this.annotations.push(this.tmp_annotations[i]);
          }
          if (this.picked === 'active') {
            if (this.tmp_annotations[i].length === 0) {
              this.docs.push(this.tmp_docs[i]);
              this.annotations.push(this.tmp_annotations[i]);
            }
          }
          if (this.picked === 'completed') {
            if (this.tmp_annotations[i].length !== 0) {
              this.docs.push(this.tmp_docs[i]);
              this.annotations.push(this.tmp_annotations[i]);
            }
          }
        }
      }
    },

    getState() {
      if (this.picked === 'all') {
        return '';
      }
      if (this.picked === 'active') {
        return 'true';
      }
      return 'false';
    },

    submit() {
      this.search();
      this.pageNumber = 0;
    },

    removeLabel(annotation) {
      const index = this.annotations[this.pageNumber].indexOf(annotation);
      this.annotations[this.pageNumber].splice(index, 1);
    },
  },

  watch: {
    picked() {
      this.submit();
    },
  },

  created() {
    this.tmp_docs = this.docs;
    this.tmp_annotations = this.annotations;
  },

  computed: {
    total() {
      return this.tmp_docs.length;
    },

    count() {
      return this.docs.length;
    },

    compiledMarkdown() {
      return marked(this.guideline, {
        sanitize: true,
      });
    },

    remaining() {
      let cnt = 0;
      for (let i = 0; i < this.tmp_annotations.length; i++) {
        if (this.tmp_annotations[i].length === 0) {
          cnt += 1;
        }
      }
      return cnt;
    },

    achievement() {
      const done = this.total - this.remaining;
      const percentage = Math.round(done / this.total * 100);
      return this.total > 0 ? percentage : 0;
    },

    id2label() {
      const id2label = {};
      for (let i = 0; i < this.labels.length; i++) {
        const label = this.labels[i];
        id2label[label.id] = label;
      }
      return id2label;
    },

    progressColor() {
      if (this.achievement < 30) {
        return 'is-danger';
      }
      if (this.achievement < 70) {
        return 'is-warning';
      }
      return 'is-primary';
    },
  },
};

export default annotationMixin;
