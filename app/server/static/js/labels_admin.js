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
      const length = dataframe.doc_ids.length;
      for (let i = 0; i < length; i++) {
        const row = {}
        row.documentId = dataframe.doc_ids[i];
        row.labelersCount = dataframe.labelers_count[i];
        row.agreementsPercent = dataframe.agreements_percent[i];
        row.topLabel = dataframe.top_label[i];
        row.lastAnnotationDate = dataframe.last_annotation_date[i];
        row.docText = dataframe.doc_text[i];
        this.tableRows.push(row)
      }
    }
  },
  created() {
    HTTP.get('labels_admin').then((response) => {
      this.formTableRows(response.data.dataframe)
    });
  },
  watch: {
  }
});
