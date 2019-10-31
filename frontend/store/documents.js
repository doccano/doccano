import DocumentService from '@/services/document.service'
import AnnotationService from '@/services/annotation.service'
import CSVParser from '@/services/parsers/csv.service'

export const state = () => ({
  items: [],
  selected: [],
  loading: false,
  selectedFormat: null,
  parsed: {},
  current: 0,
  total: 0
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
        value: 'text',
        sortable: false
      },
      {
        text: 'Metadata',
        align: 'left',
        value: 'meta',
        sortable: false
      }
    ]
  },
  parsedDoc(state) {
    if ('data' in state.parsed) {
      return state.parsed.data
    } else {
      return []
    }
  },
  currentDoc(state) {
    return state.items[state.current]
  }
}

export const mutations = {
  setCurrent(state, payload) {
    state.current = payload
  },
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
  setTotalItems(state, payload) {
    state.total = payload
  },
  parseFile(state, text) {
    const parser = new CSVParser()
    state.parsed = parser.parse(text)
  },
  addAnnotation(state, payload) {
    state.items[state.current].annotations.push(payload)
  },
  deleteAnnotation(state, annotationId) {
    state.items[state.current].annotations = state.items[state.current].annotations.filter(item => item.id !== annotationId)
  },
  updateAnnotation(state, payload) {
    const item = state.items[state.current].annotations.find(item => item.id === payload.id)
    Object.assign(item, payload)
  }
}

export const actions = {
  getDocumentList({ commit }, payload) {
    commit('setLoading', true)
    return DocumentService.getDocumentList(payload)
      .then((response) => {
        commit('setDocumentList', response.results)
        commit('setTotalItems', response.count)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  uploadDocument({ commit, dispatch }, data) {
    commit('setLoading', true)
    const formData = new FormData()
    formData.append('file', data.file)
    formData.append('format', data.format)
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    DocumentService.uploadFile(data.projectId, formData, config)
      .then((response) => {
        dispatch('getDocumentList', data)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  exportDocument({ commit }, data) {
    commit('setLoading', true)
    DocumentService.exportFile(data.projectId, data.format)
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'file.' + data.format)
        document.body.appendChild(link)
        link.click()
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
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
  nextPage({ commit }) {
  },
  prevPage({ commit }) {
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
  },
  addAnnotation({ commit, state }, payload) {
    const documentId = state.items[state.current].id
    AnnotationService.addAnnotation(payload.projectId, documentId, payload)
      .then((response) => {
        commit('addAnnotation', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateAnnotation({ commit, state }, payload) {
    const documentId = state.items[state.current].id
    AnnotationService.updateAnnotation(payload.projectId, documentId, payload.annotationId, payload)
      .then((response) => {
        commit('updateAnnotation', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteAnnotation({ commit, state }, payload) {
    const documentId = state.items[state.current].id
    AnnotationService.deleteAnnotation(payload.projectId, documentId, payload.annotationId)
      .then((response) => {
        commit('deleteAnnotation', payload.annotationId)
      })
      .catch((error) => {
        alert(error)
      })
  }
}
