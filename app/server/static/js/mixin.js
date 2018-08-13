import HTTP from './http';

const annotationMixin = {
  data() {
    return {
      cur: 0,
      items: [{
        id: null,
        text: '',
        labels: [],
      }],
      labels: [],
      guideline: '',
      total: 0,
      remaining: 0,
      searchQuery: '',
      url: '',
      picked: 'all',
      annotations: [],
    };
  },

  methods: {
    async nextPage() {
      this.cur += 1;
      if (this.cur === this.items.length) {
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

    async prevPage() {
      this.cur -= 1;
      if (this.cur === -1) {
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

    async search() {
      await HTTP.get(this.url).then((response) => {
        this.items = response.data.results;
        this.next = response.data.next;
        this.prev = response.data.previous;
      });
      for (let i = 0; i < this.items.length; i++) {
        const docId = this.items[i].id;
        HTTP.get(`docs/${docId}/annotations/`).then((response) => {
          this.annotations.push(response.data);
        });
      }
    },

    showMessage(index) {
      this.cur = index;
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
      this.cur = 0;
    },

    removeLabel(label) {
      const docId = this.items[this.cur].id;
      HTTP.delete(`docs/${docId}/annotations/${label.id}`).then((response) => {
        const index = this.annotations[this.cur].indexOf(response.data);
        this.annotations[this.cur].splice(index, 1);
      });
    },
  },

  watch: {
    picked() {
      this.submit();
    },

    items() {
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
