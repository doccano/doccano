import StatisticsService from '@/services/statistics.service'

function makeData(object, label) {
  const labels = object ? Object.keys(object) : []
  const counts = object ? Object.values(object) : []
  return {
    labels: labels,
    datasets: [{
      label: label,
      backgroundColor: '#00d1b2',
      data: counts
    }]
  }
}

export const state = () => ({
  loading: false,
  stats: {}
})

export const mutations = {
  setLoading(state, payload) {
    state.loading = payload
  },
  setStatistics(state, payload) {
    state.stats = payload
  }
}

export const getters = {
  progress(state) {
    const complete = state.stats.total - state.stats.remaining
    const incomplete = state.stats.remaining
    return {
      datasets: [{
        data: [complete, incomplete],
        backgroundColor: ['#00d1b2', '#ffdd57']
      }],

      labels: [
        'Completed',
        'Incomplete'
      ]
    }
  },
  labelStats(state) {
    return makeData(state.stats.label, 'Label stats')
  },
  userStats(state) {
    return makeData(state.stats.user, 'User stats')
  }
}

export const actions = {
  fetchStatistics({ commit }, payload) {
    commit('setLoading', true)
    StatisticsService.getStatistics(payload)
      .then((response) => {
        commit('setStatistics', response.data)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  }
}
