import HTTP from './http';
import Vue from 'vue';

Vue.component('metadata-search', {
  props: ['metadata'],
  template: `<div>
  <div class="field is-horizontal" v-for="(rule, index) in rules" :key="index">
    <div class="field-body">
      <div class="field is-narrow">
        <div class="control">
          <div class="select">
            <select v-model="rule.field">
              <option v-for="(key, index) in metadata" :value="key" :key="index">
                {{ key }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <div class="field is-narrow">
        <div class="control">
          <div class="select">
            <select  v-model="rule.comparator">
              <option v-for="comparator in comparators" :value="comparator.value" :key="comparator.value">
                {{ comparator.text }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <input class="input" type="text" placeholder="Value" v-model="rule.search">
        </div>
      </div>
    </div>
  </div>
  <div class="field">
    <div class="control">
      <button class="button is-link" @click="search" :disabled="checkDisabled">Search</button>
    </div>
  </div>
  </div>
  `,
  data() {
    return {
      comparators: [
        {text: "==", value: 'eq'},
        {text: "<=", value: 'leq'},
        {text: "<", value: 'lt'},
        {text: ">=", value: 'geq'},
        {text: ">", value: 'gt'}
      ],
      rules: [
        {field: '', comparator: 'eq', search: ''}
      ]
    };
  },
  methods: {
    search() {
      this.$emit('metadatasearch', this.rules)
    }
  },
  computed: {
    checkDisabled() {
      let ret = false
      this.rules.forEach((r) => {
        if (!r.field.length || !r.search.length) {
          ret = true
        }
      })
      return ret
    }
  }
});

const getOffsetFromUrl = function(url) {
  if (!url) {
    return 0
  }

  const params = new URLSearchParams(url);
  const offset = params.get('offset')

  if (!offset) {
    return 0
  }

  return parseInt(offset, 10);
};

const getSearchQuery = function(url) {
  if (!url) {
    return ''
  }

  const params = new URLSearchParams(url);
  const search = params.get('search')

  if (!search) {
    return ''
  }

  return search;
}

const setQueryStringParameter = (name, value) => {
  const params = new URLSearchParams(location.search);
  params.set(name, value);
  window.history.pushState({}, "", decodeURIComponent(`${location.pathname}?${params}`));
};

const storeOffsetInUrl = function(offset) {
  setQueryStringParameter('offset', offset)
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
      offset: 0,
      picked: 'all',
      count: 0,
      isActive: false,
      next: null,
      prev: null,
      highlightQuery: '',
      last: null,
      first: null,
      limit: 0,
      suggestions: [],
      explainMode: false,
      docExplanation: '',
      metadataAll: [],
      metadataKeys: [],
      metadataRules: [],
      docFromLink: null
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

    async firstDocumentsPage() {
      if (this.first) {
        this.url = this.first;
        await this.search();
        this.pageNumber = this.docs.length - 1;
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

    async lastDocumentsPage() {
      if (this.last) {
        this.url = this.last;
        await this.search();
        this.pageNumber = this.docs.length - 1;
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

    async search(setOffset = true) {
      await HTTP.get(this.url).then((response) => {
        this.docs = response.data.results;
        this.next = response.data.next;
        this.prev = response.data.previous;
        this.count = response.data.count;
        if (this.next || this.prev) {
          const limitMatches = this.next? this.next.match(/limit=(\d+)/) : this.prev.match(/limit=(\d+)/)
          this.limit = Number.parseInt(limitMatches[1], 10)
          const offsetMatches = this.next? this.next.match(/(offset=\d+)/) : this.prev.match(/(offset=\d+)/)
          const lastOffset = Math.floor(this.count / this.limit) * this.limit
          if (offsetMatches && offsetMatches.length > 1) {
            this.first = this.next ? this.next.replace(offsetMatches[1], 'offset=0') : this.prev.replace(offsetMatches[1], 'offset=0')
            this.last = this.next ? this.next.replace(offsetMatches[1], `offset=${lastOffset}`) : this.prev.replace(offsetMatches[1], `offset=${lastOffset}`)
          }
        } else {
          this.first = 0
          this.last = 0
        }
        
        
        this.annotations = [];
        for (let i = 0; i < this.docs.length; i++) {
          const doc = this.docs[i];
          this.annotations.push(doc.annotations);
        }
        
        if (setOffset) {
          this.offset = getOffsetFromUrl(this.url);
        }

        if (this.offset === 0 && this.docFromLink) {
          const docIdx = this.docs.findIndex((d) => d.id === this.docFromLink.id)
          if (docIdx === -1) {
            this.docs.unshift(this.docFromLink)
          } else {
            this.pageNumber = docIdx
          }
        }
      });
    },

    searchChange: _.debounce(function(e) {
      this.suggestions = []
      if (this.searchQuery.length > 2) {
        const splittedQuery = this.searchQuery.trim().split(' ')
        const lastWord = splittedQuery[splittedQuery.length - 1]
        this.getSuggestions(lastWord)
      }
    }, 500),

    async getSuggestions(word) {
      const res = await HTTP.get(`suggested/?word=${word}`)
      if (res && res.data) {
        this.suggestions = res.data
      }
    },

    async submitSuggestion(s) {
      const suggestion = s[0]
      if (this.searchQuery[this.searchQuery.length - 1] === ' ') {
        this.searchQuery += suggestion
      } else {
        this.searchQuery += ` ${suggestion}`
      }
      this.suggestions = []
      await this.getSuggestions(suggestion)
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
      this.suggestions = []
      this.url = `docs/?q=${this.searchQuery}&is_checked=${state}&offset=${this.offset}&rules=${JSON.stringify(this.metadataRules)}`;
      await this.search();
      this.pageNumber = 0;

      if (this.explainMode) {
        const doc = this.docs[0]
        if (doc) {
          this.getExplanation(doc.id)
        }
      }

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

    getExplanation(id) {
      HTTP.get(`docs/${id}/explanation`).then((response) => {
        if (response.data) {
          this.docExplanation = response.data.document
        }
      });
    },

    async popState() {
      const offset = getOffsetFromUrl(location.search)
      const searchQuery = getSearchQuery(location.search)
      const state = this.getState();
      this.url = `docs/?q=${searchQuery}&is_checked=${state}&offset=${offset}&rules=${JSON.stringify(this.metadataRules)}`;
      await this.search(false);
    },

    async metadataSearch(rules) {
      this.metadataRules = rules
      await this.submit()
    }
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

    explainMode(val) {
      if (val) {
        localStorage.setItem('doccano_explainMode', true)
        const doc = this.docs[this.pageNumber]
        this.getExplanation(doc.id)
      } else {
        localStorage.removeItem('doccano_explainMode')
      }
    },

    pageNumber(val) {
      if (this.explainMode) {
        const doc = this.docs[val]
        this.getExplanation(doc.id)
      }
    }
  },

  async created() {
    this.offset = getOffsetFromUrl(location.search)
    this.searchQuery = getSearchQuery(location.search)
    HTTP.get('labels').then((response) => {
      this.labels = response.data;
    });
    HTTP.get().then((response) => {
      this.guideline = response.data.guideline;
    });
    HTTP.get('metadata').then((response) => {
      response.data.metadata.forEach((m) => {
        try {
          const data = JSON.parse(m);
          Object.keys(data).forEach((k) => {
            if (!this.metadataKeys.includes(k)) {
              this.metadataKeys.push(k);
            }
          })
        } catch (e) {
          console.log('Wrong metadata format')
        }
      })
    });

    if (location.hash && location.hash.length) {
      if (location.hash.indexOf('#document=') !== -1) {
        try {
          const docResp = await HTTP.get(`docs/${location.hash.replace('#document=', '')}`)
          this.docFromLink = docResp.data
        } catch(e) {
          this.docFromLink = null
        }
      }
    }

    const state = this.getState();
    this.url = `docs/?q=${this.searchQuery}&is_checked=${state}&offset=${this.offset}`;
    await this.search();
    
    if (localStorage) {
      const explainMode = localStorage.getItem('doccano_explainMode')
      if (explainMode) {
        this.explainMode = true
      }
    }

    if (this.explainMode) {
      const doc = this.docs[0]
      this.getExplanation(doc.id)
    }

    window.addEventListener('popstate', this.popState)
  },

  beforeDestroy() {
    window.removeEventListener('popstate', this.popState)
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

    currentDoc() {
      if (this.pageNumber >= 0) {
        return this.docs[this.pageNumber];
      }
      return null;
    },

    metadataString() {
      if (this.currentDoc && this.currentDoc.metadata) {
        const json = JSON.parse(this.currentDoc.metadata)
        const str = JSON.stringify(json, undefined, 4);
        return syntaxHighlight(str);
      }
      return null;
    },

    docText() {
      let text = this.docs[this.pageNumber].text;

      if (this.explainMode && this.docExplanation) {
        text = this.docExplanation
      }

      if(this.highlightQuery.length) {
        const complexSearchRegex = /^\"(.*)\"\s*(\-)?(.*$)/;
        const complexMatches = this.highlightQuery.match(complexSearchRegex)
        let terms = this.highlightQuery.split(' ');
        if (complexMatches && complexMatches[1] && complexMatches[3]) {
          terms = [complexMatches[1], complexMatches[3]]
        } else if (complexMatches && complexMatches[1]) {
          terms = [complexMatches[1]]
        }
        terms.forEach((term) => {
          text = text.replace(new RegExp(`(${term})`, 'gi'), `<span class="highlight">$1</span>`)
        });
      }
      
      return text
    },

    currentPage() {
      if (this.offset && this.limit) {
        return this.offset / this.limit
      }
      return 0
    },

    lastPage() {
      return Math.floor(this.count / this.limit)
    },


    predictedLabel() {
      if (this.currentDoc && this.currentDoc.mlm_annotations && this.currentDoc.mlm_annotations.length) {
        const pred = this.currentDoc.mlm_annotations[0]
        const label = this.labels.find((l) => l.id === pred.label)
        const { prob } = pred
        return {
          label,
          prob
        }
      }
      return null
    }
  },
};

export default annotationMixin;
