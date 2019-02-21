import HTTP from './http';

const getOffsetFromUrl = function(url) {
  const offsetMatch = url.match(/[?#].*offset=(\d+)/);
  if (offsetMatch == null) {
    return 0;
  }

  return parseInt(offsetMatch[1], 10);
};

const storeOffsetInUrl = function(offset) {
  let href = window.location.href;

  const fragmentStart = href.indexOf('#') + 1;
  if (fragmentStart === 0) {
    href += '#offset=' + offset;
  } else {
    const prefix = href.substring(0, fragmentStart);
    const fragment = href.substring(fragmentStart);

    const newFragment = fragment.split('&').map(function(fragmentPart) {
      const keyValue = fragmentPart.split('=');
      return keyValue[0] === 'offset'
        ? 'offset=' + offset
        : fragmentPart;
    }).join('&');

    href = prefix + newFragment;
  }

  window.location.href = href;
};

const syntaxHighlight = (json) => {
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
      var cls = 'number';
      if (/^"/.test(match)) {
          if (/:$/.test(match)) {
              cls = 'key';
          } else {
              cls = 'string';
          }
      } else if (/true|false/.test(match)) {
          cls = 'boolean';
      } else if (/null/.test(match)) {
          cls = 'null';
      }
      return '<span class="' + cls + '">' + match + '</span>';
  });
}

const annotationMixin = {
  data() {
    return {
      pageNumber: 0,
      docs: [],
      annotations: [],
      labels: [],
      guideline: '',
      total: 0,
      remaining: 0,
      searchQuery: '',
      url: '',
      offset: getOffsetFromUrl(window.location.href),
      picked: 'all',
      count: 0,
      isActive: false,
      next: null,
      prev: null,
      highlightQuery: '',
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

    async prevDocumentsPage() {
      if (this.prev) {
        this.url = this.prev;
        await this.search();
        this.pageNumber = this.docs.length - 1;
      }
    },

    async nextDocumentsPage() {
      if (this.next) {
        this.url = this.next;
        await this.search();
        this.pageNumber = 0;
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
        this.count = response.data.count;
        this.annotations = [];
        for (let i = 0; i < this.docs.length; i++) {
          const doc = this.docs[i];
          this.annotations.push(doc.annotations);
        }
        this.offset = getOffsetFromUrl(this.url);
      });
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
      this.offset = 0;
      this.url = `docs/?q=${this.searchQuery}&is_checked=${state}&offset=${this.offset}`;
      await this.search();
      this.pageNumber = 0;

      if (this.searchQuery.length) {
        this.highlightQuery = this.searchQuery;
      } else {
        this.highlightQuery = '';
      }
    },

    removeLabel(annotation) {
      const docId = this.docs[this.pageNumber].id;
      HTTP.delete(`docs/${docId}/annotations/${annotation.id}`).then((response) => {
        const index = this.annotations[this.pageNumber].indexOf(annotation);
        this.annotations[this.pageNumber].splice(index, 1);
      });
    },

    replaceNull(shortcut) {
      if (shortcut === null) {
        shortcut = '';
      }
      shortcut = shortcut.split(' ');
      return shortcut;
    },
  },

  watch: {
    picked() {
      this.submit();
    },

    annotations() {
      // fetch progress info.
      HTTP.get('progress').then((response) => {
        this.total = response.data.total;
        this.remaining = response.data.remaining;
      });
    },

    offset() {
      storeOffsetInUrl(this.offset);
    },
  },

  created() {
    HTTP.get('labels').then((response) => {
      this.labels = response.data;
    });
    HTTP.get().then((response) => {
      this.guideline = response.data.guideline;
    });
    this.submit();
  },

  computed: {
    achievement() {
      const done = this.total - this.remaining;
      const percentage = Math.round(done / this.total * 100);
      return this.total > 0 ? percentage : 0;
    },

    compiledMarkdown() {
      return marked(this.guideline, {
        sanitize: true,
      });
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

    metadataString() {
      if (this.pageNumber && this.docs[this.pageNumber] && this.docs[this.pageNumber].metadata) {
        const json = JSON.parse(this.docs[this.pageNumber].metadata)
        const str = JSON.stringify(json, undefined, 4);
        return syntaxHighlight(str);
      }

      return null;
    },

    docText() {
      if(this.highlightQuery.length) {
        let text = this.docs[this.pageNumber].text;
        const complexSearchRegex = /^\"(.*)\"\s*\-?(.*$)/;
        const complexMatches = this.highlightQuery.match(complexSearchRegex)
        let terms = this.highlightQuery.split(' ');
        if (complexMatches && complexMatches[1]) {
          terms = [complexMatches[1]]
        }
        terms.forEach((term) => {
          text = text.replace(new RegExp(term, 'g'), `<span class="highlight">${term}</span>`)
        });
        return text
      }
      return this.docs[this.pageNumber].text 
    }
  },
};

export default annotationMixin;
