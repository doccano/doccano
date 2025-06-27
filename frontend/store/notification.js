export const state = () => ({
  show: false,
  text: '',
  color: 'info',
  timeout: 4000
})

export const mutations = {
  setNotification(state, { text, color = 'info', timeout = 4000 }) {
    state.text = text
    state.color = color
    state.timeout = timeout
    state.show = true
  },
  hideNotification(state) {
    state.show = false
  }
}

export const actions = {
  setNotification({ commit }, payload) {
    commit('setNotification', payload)
  },
  hideNotification({ commit }) {
    commit('hideNotification')
  }
}

export const getters = {
  show(state) {
    return state.show
  },
  text(state) {
    return state.text
  },
  color(state) {
    return state.color
  },
  timeout(state) {
    return state.timeout
  }
}
