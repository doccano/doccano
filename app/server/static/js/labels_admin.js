import Vue from 'vue';
import HTTP from './http';

Vue.component('th-sortable', {
  props: ['label', 'field', 'value'],
  template: `
  <th @click="toggleSort">
    {{ label }}
    <span class="icon" v-if="value.field == field && value.order == 'asc'">
      <i class="fas fa-sort-up" aria-hidden="true"></i>
    </span>
    <span class="icon" v-if="value.field == field && value.order == 'desc'">
      <i class="fas fa-sort-down" aria-hidden="true"></i>
    </span>
  </th>`,
  data() {
    return {
      labels: []
    };
  },
  methods: {
    toggleSort() {
      if (this.value && this.value.field === this.field) {
        if (this.value.order === 'asc') {
          this.$emit('input', { field: this.field, order: 'desc' })
        } else {
          this.$emit('input', {})
        }
      } else {
        this.$emit('input', { field: this.field, order: 'asc' })
      }
    }
  }
});

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    tableRows: [],
    sort: {}
  },

  computed: {
    filteredTableRows() {
      let listClone = this.tableRows.slice()
      if (this.sort && this.sort.field) {
        listClone = listClone.sort((a, b) => {
          const fieldA = a[this.sort.field]
          const fieldB = b[this.sort.field]
          const order = this.sort.order === 'desc' ? -1 : 1

          if (fieldA > fieldB) {
            return order
          } else if(fieldA < fieldB) {
            return -1 * order
          }

          return 0
        })
      }


      return listClone;
    }
  },
  
  methods: {
    formTableRows(dataframe) {
      const length = dataframe.document_id.length;
      for (let i = 0; i < length; i++) {
        const row = {}
        row.documentId = dataframe.document_id[i];
        row.labelersCount = dataframe.num_labelers[i];
        row.agreementsPercent = dataframe.agreement[i];
        row.topLabel = this.labelNameById(dataframe.top_label[i]);
        row.lastAnnotationDate = dataframe.last_annotation_date[i];
        row.snippet = dataframe.snippet[i];
        this.tableRows.push(row)
      }
    },
    labelNameById(id) {
      const label = this.labels.find((l) => +l.id === +id)
      if (label) {
        return label.text
      }

      return ''
    },
    getUrl(base, docId) {
      return `${base}#document=${docId}`
    }
  },
  async created() {
    const la = await HTTP.get('labels_admin')
    const labels = await HTTP.get('labels')
    this.labels = labels.data
    this.formTableRows(la.data.dataframe)
  },
  watch: {
  }
});
