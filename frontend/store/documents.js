import DocumentService from '@/services/document.service'
import CSVParser from '@/services/parsers/csv.service'

export const state = () => ({
  items: [],
  selected: [],
  loading: false,
  selectedFormat: null,
  parsed: {}
})

export const getters = {
  isDocumentSelected(state) {
    return state.selected.length > 0
  },
  formatList() {
    return [
      {
        type: 'csv',
        text: 'Upload a CSV file from your computer',
        accept: '.csv'
      },
      {
        type: 'plain',
        text: 'Upload text items from your computer',
        accept: '.txt'
      },
      {
        type: 'json',
        text: 'Upload a JSON file from your computer',
        accept: '.json,.jsonl'
      }
    ]
  },
  headers() {
    return [
      {
        text: 'Text',
        align: 'left',
        value: 'text'
      },
      {
        text: 'Metadata',
        align: 'left',
        value: 'meta'
      }
    ]
  },
  parsedDoc(state) {
    if ('data' in state.parsed) {
      return state.parsed.data
    } else {
      return []
    }
  }
}

export const mutations = {
  setDocumentList(state, payload) {
    state.items = payload
  },
  addDocument(state, document) {
    state.items.unshift(document)
  },
  deleteDocument(state, documentId) {
    state.items = state.items.filter(item => item.id !== documentId)
  },
  updateSelected(state, selected) {
    state.selected = selected
  },
  updateDocument(state, document) {
    const item = state.items.find(item => item.id === document.id)
    Object.assign(item, document)
  },
  resetSelected(state) {
    state.selected = []
  },
  setLoading(state, payload) {
    state.loading = payload
  },
  parseFile(state, text) {
    const parser = new CSVParser()
    state.parsed = parser.parse(text)
  }
}

export const actions = {
  getDocumentList({ commit }, config) {
    commit('setLoading', true)
    return DocumentService.getDocumentList()
      .then((response) => {
        commit('setDocumentList', response)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  uploadDocument({ commit }, data) {
    DocumentService.addDocument(data.projectId, data)
      .then((response) => {
        commit('addDocument', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateDocument({ commit }, data) {
    DocumentService.updateDocument(data.projectId, data.id, data)
      .then((response) => {
        commit('updateDocument', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteDocument({ commit, state }, projectId) {
    for (const document of state.selected) {
      DocumentService.deleteDocument(projectId, document.id)
        .then((response) => {
          commit('deleteDocument', document.id)
        })
        .catch((error) => {
          alert(error)
        })
    }
    commit('resetSelected')
  },
  parseFile({ commit }, data) {
    const reader = new FileReader()
    reader.readAsText(data, 'UTF-8')
    reader.onload = (e) => {
      commit('parseFile', e.target.result)
    }
    reader.onerror = (e) => {
      alert(e)
    }
  }
}
