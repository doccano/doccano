import * as marked from 'marked';
import VueJsonPretty from 'vue-json-pretty';
import isEmpty from 'lodash.isempty';
import HTTP from './http';
import Preview from './preview.vue';

const getOffsetFromUrl = (url) => {
  const offsetMatch = url.match(/[?#].*offset=(\d+)/);
  if (offsetMatch == null) {
    return 0;
  }

  return parseInt(offsetMatch[1], 10);
};

const removeHost = (url) => {
  if (!url) {
    return url;
  }

  const hostMatch = url.match(/^https?:\/\/[^/]*\/(.*)$/);
  if (hostMatch == null) {
    return url;
  }

  return `${window.location.origin}/${hostMatch[1]}`;
};

const storeOffsetInUrl = (offset) => {
  let href = window.location.href;

  const fragmentStart = href.indexOf('#') + 1;
  if (fragmentStart === 0) {
    href += '#offset=' + offset;
  } else {
    const prefix = href.substring(0, fragmentStart);
    const fragment = href.substring(fragmentStart);

    const newFragment = fragment.split('&').map((fragmentPart) => {
      const keyValue = fragmentPart.split('=');
      return keyValue[0] === 'offset'
        ? 'offset=' + offset
        : fragmentPart;
    }).join('&');

    href = prefix + newFragment;
  }

  window.location.href = href;
};

const getLimitFromUrl = (url, prevLimit) => {
  try {
    const limitMatch = url.match(/[?#].*limit=(\d+)/);

    return parseInt(limitMatch[1], 10);
  } catch (err) {
    return prevLimit;
  }
};

const getSidebarTotal = (count, limit) => (
  count !== 0 && limit !== 0
    ? Math.ceil(count / limit)
    : 0
);

const getSidebarPage = (offset, limit) => (
  limit !== 0
    ? Math.ceil(offset / limit) + 1
    : 0
);

export default {
  components: { VueJsonPretty, Preview },

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
      prevLimit: 0,
      paginationPages: 0,
      paginationPage: 0,
      isAnnotationApprover: false,
      isMetadataActive: false,
      isAnnotationGuidelineActive: false,
    };
  },

  methods: {
    resetScrollbar() {
      const textbox = this.$refs.textbox;
      if (textbox) {
        textbox.scrollTop = 0;
      }
    },

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
      } else {
        this.resetScrollbar();
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
      } else {
        this.resetScrollbar();
      }
    },

    async nextPagination() {
      if (this.next) {
        this.url = this.next;
        await this.search();
        this.pageNumber = 0;
      } else {
        this.pageNumber = this.docs.length - 1;
      }
      this.resetScrollbar();
    },

    async prevPagination() {
      if (this.prev) {
        this.url = this.prev;
        await this.search();
        this.pageNumber = this.docs.length - this.limit;
      } else {
        this.pageNumber = 0;
      }
      this.resetScrollbar();
    },

    async search() {
      await HTTP.get(this.url).then((response) => {
        this.docs = response.data.results;
        this.next = removeHost(response.data.next);
        this.prev = removeHost(response.data.previous);
        this.count = response.data.count;
        this.annotations = this.docs.map(doc => doc.annotations);
        this.offset = getOffsetFromUrl(this.url);
        this.prevLimit = this.limit;
        if (this.next || this.prevLimit) {
          this.limit = getLimitFromUrl(this.next, this.prevLimit);
        } else {
          this.limit = this.count;
        }
        this.paginationPages = getSidebarTotal(this.count, this.limit);
        this.paginationPage = getSidebarPage(this.offset, this.limit);
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
      this.url = `docs?q=${this.searchQuery}&is_checked=${state}&offset=${this.offset}`;
      await this.search();
      this.pageNumber = 0;
    },

    removeLabel(annotation) {
      const docId = this.docs[this.pageNumber].id;
      HTTP.delete(`docs/${docId}/annotations/${annotation.id}`).then(() => {
        const index = this.annotations[this.pageNumber].indexOf(annotation);
        this.annotations[this.pageNumber].splice(index, 1);
      });
    },

    replaceNull(shortcut) {
      if (shortcut == null) {
        shortcut = '';
      }
      shortcut = shortcut.split(' ');
      return shortcut;
    },

    shortcutKey(label) {
      let shortcut = label.suffix_key;
      if (label.prefix_key) {
        shortcut = `${label.prefix_key} ${shortcut}`;
      }
      return shortcut;
    },

    approveDocumentAnnotations() {
      const document = this.docs[this.pageNumber];
      const approved = !this.documentAnnotationsAreApproved;

      HTTP.post(`docs/${document.id}/approve-labels`, { approved }).then((response) => {
        const documents = this.docs.slice();
        documents[this.pageNumber] = response.data;
        this.docs = documents;
      });
    },
  },

  watch: {
    picked() {
      this.submit();
    },

    annotations() {
      // fetch progress info.
      HTTP.get('statistics').then((response) => {
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
      const roles = response.data.current_users_role;
      this.isAnnotationApprover = roles.is_annotation_approver || roles.is_project_admin;
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

    documentAnnotationsAreApproved() {
      const document = this.docs[this.pageNumber];
      return document != null && document.annotation_approver != null;
    },

    documentAnnotationsApprovalTooltip() {
      const document = this.docs[this.pageNumber];

      return this.documentAnnotationsAreApproved
        ? `Annotations approved by ${document.annotation_approver}, click to reject annotations`
        : 'Click to approve annotations';
    },

    documentMetadata() {
      const document = this.docs[this.pageNumber];
      if (document == null || document.meta == null) {
        return null;
      }

      const metadata = JSON.parse(document.meta);
      if (isEmpty(metadata)) {
        return null;
      }

      return metadata;
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
