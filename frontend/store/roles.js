import RoleService from '@/services/role.service'

export const state = () => ({
  items: [],
  loading: false
})

export const getters = {
  roles(state) {
    return state.items
  }
}

export const mutations = {
  setRoleList(state, payload) {
    state.items = payload
  },
  setLoading(state, payload) {
    state.loading = payload
  }
}

export const actions = {
  getRoleList({ commit }) {
    commit('setLoading', true)
    return RoleService.getRoleList()
      .then((response) => {
        commit('setRoleList', response.data)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  }
}
