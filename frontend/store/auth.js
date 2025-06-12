export const state = () => ({
  username: null,
  id: null,
  isAuthenticated: false,
  isStaff: false
})

export const mutations = {
  setUsername(state, username) {
    state.username = username
  },
  setUserId(state, userId) {
    state.id = userId
  },
  clearUsername(state) {
    state.username = null
  },
  setAuthenticated(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated
  },
  setIsStaff(state, isStaff) {
    state.isStaff = isStaff
  },
  setIsSuperUser(state, isSuperUser) {
    state.isSuperUser = isSuperUser
  }
}

export const getters = {
  isAuthenticated(state) {
    return state.isAuthenticated
  },
  getUsername(state) {
    return state.username
  },
  getUserId(state) {
    return state.id
  },
  isStaff(state) {
    return state.isStaff
  },
  isSuperUser(state) {
    return state.isSuperUser
  }
}

export const actions = {
  async authenticateUser({ commit }, authData) {
    console.log('authData', authData)
    try {
      await this.$repositories.auth.login(authData.username, authData.password)
      commit('setAuthenticated', true)
    } catch (error) {
      throw new Error('The credential is invalid')
    }
  },
  async fetchSocialLink() {
    return await this.$repositories.auth.socialLink()
  },
  async initAuth({ commit }) {
    try {
      const user = await this.$repositories.user.getProfile()
      commit('setAuthenticated', true)
      commit('setUsername', user.username)
      commit('setUserId', user.id)
      commit('setIsStaff', user.isStaff)
      commit('setIsSuperUser', user.isSuperUser)
    } catch {
      commit('setAuthenticated', false)
      commit('setIsStaff', false)
    }
  },
  async logout({ commit }) {
    await this.$repositories.auth.logout()
    commit('setAuthenticated', false)
    commit('setIsStaff', false)
    commit('clearUsername')
  },
  async registerUser(_, authData) {
    console.log('authData', authData)
    try {
      await this.$repositories.auth.register(
        authData.username, 
        authData.firstName,
        authData.lastName,
        authData.email, 
        authData.password, 
        authData.passwordConfirm
      )
    } catch (error) {
      console.log('Register error:', error)
      
      // Se temos dados de resposta do servidor, vamos processar os erros
      if (error.response && error.response.data) {
        const errors = error.response.data
        let errorMessage = ''
        
        // Verificar erros específicos de cada campo
        if (errors.password) {
          const passwordErrors = Array.isArray(errors.password) ? errors.password : [errors.password]
          for (const passwordError of passwordErrors) {
            if (typeof passwordError === 'string') {
              if (passwordError.includes('too common') || passwordError.includes('common')) {
                errorMessage = 'A palavra-passe é muito comum. Use uma palavra-passe mais segura.'
              } else if (passwordError.includes('too short')) {
                errorMessage = 'A palavra-passe é muito curta. Use pelo menos 8 caracteres.'
              } else if (passwordError.includes('numeric')) {
                errorMessage = 'A palavra-passe não pode ser apenas numérica.'
              } else if (passwordError.includes('similar')) {
                errorMessage = 'A palavra-passe é muito semelhante às suas informações pessoais.'
              } else {
                errorMessage = `Erro na palavra-passe: ${passwordError}`
              }
              break
            }
          }
        } else if (errors.username) {
          const usernameErrors = Array.isArray(errors.username) ? errors.username : [errors.username]
          if (usernameErrors[0].includes('already exists') || usernameErrors[0].includes('username already exists')) {
            errorMessage = 'Este username já está em uso. Use um username diferente.'
          } else {
            errorMessage = `Erro no nome de utilizador: ${usernameErrors[0]}`
          }
        } else if (errors.email) {
          const emailErrors = Array.isArray(errors.email) ? errors.email : [errors.email]
          if (emailErrors[0].includes('already exists')) {
            errorMessage = 'Este email já está em uso. Use um email diferente.'
          } else {
            errorMessage = `Erro no email: ${emailErrors[0]}`
          }
        } else if (errors.password_confirm) {
          errorMessage = 'As palavras-passe não coincidem.'
        } else {
          errorMessage = 'Falha ao registar utilizador. Verifique os dados inseridos.'
        }
        
        throw new Error(errorMessage)
      }
      
      throw new Error('Falha ao registar utilizador. Verifique a ligação ao servidor.')
    }
  }
}
