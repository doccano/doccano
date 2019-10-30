import ProjectService from '@/services/project.service'

export const state = () => ({
  projects: [],
  selected: [],
  current: {},
  loading: false
})

export const getters = {
  isProjectSelected(state) {
    return state.selected.length > 0
  },
  currentProject(state) {
    return state.current
  },
  headers() {
    return [
      {
        text: 'Name',
        align: 'left',
        value: 'name'
      },
      {
        text: 'Description',
        value: 'description'
      },
      {
        text: 'Type',
        value: 'project_type'
      }
    ]
  },
  getUploadFormat(state) {
    const plain = {
      type: 'plain',
      text: 'Plain text',
      accept: '.txt',
      examples: [
        'EU rejects German call to boycott British lamb.\n',
        'Peter Blackburn\n',
        'President Obama'
      ]
    }
    const csv = {
      type: 'csv',
      text: 'CSV',
      accept: '.csv'
    }
    const json = {
      type: 'json',
      text: 'JSON',
      accept: '.json,.jsonl'
    }
    const conll = {
      type: 'conll',
      text: 'CoNLL',
      accept: '.conll'
    }
    if (state.current.project_type === 'DocumentClassification') {
      json.examples = [
        '{"text": "Terrible customer service.", "labels": ["negative"]}\n',
        '{"text": "Really great transaction.", "labels": ["positive"]}\n',
        '{"text": "Great price.", "labels": ["positive"]}'
      ]
      csv.examples = [
        'text,label\n',
        '"Terrible customer service.","negative"\n',
        '"Really great transaction.","positive"\n',
        '"Great price.","positive"'
      ]
      return [
        plain,
        csv,
        json
      ]
    } else if (state.current.project_type === 'SequenceLabeling') {
      json.examples = [
        '{"text": "EU rejects German call to boycott British lamb.", "labels": [ [0, 2, "ORG"], [11, 17, "MISC"], ... ]}\n',
        '{"text": "Peter Blackburn", "labels": [ [0, 15, "PERSON"] ]}\n',
        '{"text": "President Obama", "labels": [ [10, 15, "PERSON"] ]}'
      ]
      conll.examples = [
        'EU\tB-ORG\n',
        'rejects\tO\n',
        'German\tB-MISC\n',
        'call\tO\n',
        'to\tO\n',
        'boycott\tO\n',
        'British\tB-MISC\n',
        'lamb\tO\n',
        '.\tO\n\n',
        'Peter\tB-PER\n',
        'Blackburn\tI-PER'
      ]
      return [
        plain,
        json,
        conll
      ]
    } else if (state.current.project_type === 'Seq2seq') {
      json.examples = [
        '{"text": "Hello!", "labels": ["こんにちは！"]}\n',
        '{"text": "Good morning.", "labels": ["おはようございます。"]}\n',
        '{"text": "See you.", "labels": ["さようなら。"]}'
      ]
      csv.examples = [
        'text,label\n',
        '"Hello!","こんにちは！"\n',
        '"Good morning.","おはようございます。"\n',
        '"See you.","さようなら。"'
      ]
      return [
        plain,
        csv,
        json
      ]
    } else {
      return []
    }
  }
}

export const mutations = {
  setProjectList(state, payload) {
    state.projects = payload
  },
  createProject(state, project) {
    state.projects.unshift(project)
  },
  updateProject(state, project) {
    const item = state.projects.find(item => item.id === project.id)
    Object.assign(item, project)
  },
  deleteProject(state, projectId) {
    state.projects = state.projects.filter(item => item.id !== projectId)
  },
  updateSelected(state, selected) {
    state.selected = selected
  },
  resetSelected(state) {
    state.selected = []
  },
  setLoading(state, payload) {
    state.loading = payload
  },
  setCurrent(state, payload) {
    state.current = payload
  }
}

export const actions = {
  getProjectList({ commit }, config) {
    commit('setLoading', true)
    ProjectService.getProjectList()
      .then((response) => {
        commit('setProjectList', response)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  createProject({ commit }, project) {
    ProjectService.createProject(project)
      .then((response) => {
        commit('createProject', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateProject({ commit }, data) {
    ProjectService.updateProject(data.projectId, data)
      .then((response) => {
        commit('updateProject', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteProject({ commit, state }, config) {
    for (const project of state.selected) {
      ProjectService.deleteProject(project.id)
        .then((response) => {
          commit('deleteProject', project.id)
        })
        .catch((error) => {
          alert(error)
        })
    }
    commit('resetSelected')
  },
  setCurrentProject({ commit }, projectId) {
    return ProjectService.fetchProjectById(projectId)
      .then((response) => {
        commit('setCurrent', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateCurrentProject({ commit }, data) {
    ProjectService.updateProject(data.projectId, data)
      .then((response) => {
        commit('setCurrent', response)
      })
      .catch((error) => {
        alert(error)
      })
  }
}
