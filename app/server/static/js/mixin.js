import HTTP from './http';

const annotationMixin = {
  data() {
    return {
      pageNumber: 0,
      docs: [{
        id: null,
        text: '',
      }],
      annotations: [],
      labels: [],
      guideline: '',
      total: 0,
      remaining: 0,
      searchQuery: '',
      url: '',
      picked: 'all',
    };
  },

  methods: {
    async nextPage() {
      this.pageNumber += 1;
      if (this.pageNumber === this.docs.length) {
        if (this.next) {
          this.url = this.next;
          await this.search();
          this.pageNumber = 0;
        } else {
          this.pageNumber = this.docs.length - 1;
        }
      }
    },

    async prevPage() {
      this.pageNumber -= 1;
      if (this.pageNumber === -1) {
        if (this.prev) {
          this.url = this.prev;
          await this.search();
          this.pageNumber = this.docs.length - 1;
        } else {
          this.pageNumber = 0;
        }
      }
    },

    async search() {
      await HTTP.get(this.url).then((response) => {
        this.docs = response.data.results;
        this.next = response.data.next;
        this.prev = response.data.previous;
      });
      for (let i = 0; i < this.docs.length; i++) {
        const docId = this.docs[i].id;
        HTTP.get(`docs/${docId}/annotations/`).then((response) => {
          this.annotations.push(response.data);
        });
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

    async submit() {
      const state = this.getState();
      this.url = `docs/?q=${this.searchQuery}&is_checked=${state}`;
      await this.search();
      this.pageNumber = 0;
    },

    removeLabel(label) {
      const docId = this.docs[this.pageNumber].id;
      HTTP.delete(`docs/${docId}/annotations/${label.id}`).then((response) => {
        const index = this.annotations[this.pageNumber].indexOf(response.data);
        this.annotations[this.pageNumber].splice(index, 1);
      });
    },
  },

  watch: {
    picked() {
      this.submit();
    },

    docs() {
      // fetch progress info.
      HTTP.get('progress').then((response) => {
        this.total = response.data.total;
        this.remaining = response.data.remaining;
      });
    },
  },

  created() {
    HTTP.get('labels').then((response) => {
      this.labels = response.data;
    });
    this.submit();
  },

  computed: {
    achievement() {
      const done = this.total - this.remaining;
      const percentage = Math.round(done / this.total * 100);
      return this.total > 0 ? percentage : 0;
    },

    id2label() {
      let id2label = {};
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
