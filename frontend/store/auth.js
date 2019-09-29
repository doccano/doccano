import Cookie from 'js-cookie'

export const state = () => ({
  token: null
})

export const mutations = {
  setToken(state, token) {
    state.token = token
  },
  clearToken(state) {
    state.token = null
  }
}

export const getters = {
  isAuthenticated(state) {
    return state.token != null
  }
}

export const actions = {
  authenticateUser({ commit }, authData) {
    let authUrl =
      'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=' +
      process.env.fbAPIKey
    if (!authData.isLogin) {
      authUrl =
        'https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=' +
        process.env.fbAPIKey
    }
    return this.$axios
      .$post(authUrl, {
        email: authData.email,
        password: authData.password,
        returnSecureToken: true
      })
      .then((result) => {
        commit('setToken', result.idToken)
        localStorage.setItem('token', result.idToken)
        localStorage.setItem(
          'tokenExpiration',
          new Date().getTime() + Number.parseInt(result.expiresIn) * 1000
        )
        Cookie.set('jwt', result.idToken)
        Cookie.set(
          'expirationDate',
          new Date().getTime() + Number.parseInt(result.expiresIn) * 1000
        )
      })
      .catch(e => alert(e))
  },
  initAuth({ commit, dispatch }, req) {
    let token
    let expirationDate
    if (req) {
      if (!req.headers.cookie) {
        return
      }
      const jwtCookie = req.headers.cookie
        .split(';')
        .find(c => c.trim().startsWith('jwt='))
      if (!jwtCookie) {
        return
      }
      token = jwtCookie.split('=')[1]
      expirationDate = req.headers.cookie
        .split(';')
        .find(c => c.trim().startsWith('expirationDate='))
        .split('=')[1]
    } else {
      token = localStorage.getItem('token')
      expirationDate = localStorage.getItem('tokenExpiration')
    }
    if (new Date().getTime() > +expirationDate || !token) {
      dispatch('logout')
      return
    }
    commit('setToken', token)
  },
  logout({ commit }) {
    commit('clearToken')
    Cookie.remove('jwt')
    Cookie.remove('expirationDate')
    if (process.client) {
      localStorage.removeItem('token')
      localStorage.removeItem('tokenExpiration')
    }
  }
}
