export const state = () => ({
  rtl: false
})

export const mutations = {
  changeRTLState(state) {
    state.rtl = !state.rtl
  }
}

export const getters = {
  isRTL(state) {
    return state.rtl
  }
}

export const actions = {
  toggleRTL({ commit }) {
    commit('changeRTLState')
  }
}
