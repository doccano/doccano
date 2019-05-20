import Vue from 'vue';
import HTTP from './http';

import { VueGoodTable } from 'vue-good-table';

import { toPercent } from './filters'

import 'vue-good-table/dist/vue-good-table.css'

Vue.filter('toPercent', toPercent)

const addZero = (str) => {
  return ('0'+str).substr(-2)
}

const parseDate = (date) => {
  const dateParsed = new Date(date)
  return dateParsed.getFullYear() + "/" + (dateParsed.getMonth() + 1) + "/" + dateParsed.getDate() + " " + addZero(dateParsed.getHours()) + ":" + addZero(dateParsed.getMinutes()) + ":" + addZero(dateParsed.getSeconds()) 
}

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    tableRows: [],
    sort: {},
    tableColumns: [
      {
        label: 'Document Id',
        field: 'documentId',
        type: 'number'
      },
      {
        label: 'Label',
        field: 'topLabel'
      },
      {
        label: 'Ground Truth',
        field: 'groundTruth'
      },
      {
        label: 'Model Confidence',
        field: 'modelConfidence',
        type: 'percentage'
      },
      {
        label: 'Annotation Date',
        field: 'lastAnnotationDate',
        type: 'date',
        dateInputFormat: 'YYYY/M/D HH:mm:ss',
        dateOutputFormat: 'YYYY/M/D HH:mm:ss'
      },
      {
        label: 'Snippet',
        field: 'snippet'
      }
    ]
  },

  components: {
    VueGoodTable
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
        row.groundTruth = this.labelNameById(dataframe.ground_truth[i]);
        row.modelConfidence = dataframe.model_confidence[i];
        row.lastAnnotationDate = parseDate(dataframe.last_annotation_date[i]);
        row.docText = dataframe.snippet[i];
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
    const locSpl = window.location.href.split('/')
    this.userId = +locSpl[locSpl.length - 1]

    const la = await HTTP.get(`users/${this.userId}`)
    const labels = await HTTP.get('labels')
    this.labels = labels.data
    this.formTableRows(la.data.dataframe)
  },
  watch: {
  }
});
