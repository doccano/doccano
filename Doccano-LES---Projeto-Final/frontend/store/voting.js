export const state = () => ({
  activeVoting: null,
  pastVotings: [],
  annotationRules: [],
  votes: {} // Armazenar votos por regra e usuário: { ruleId: { userId: 'aprovar|rejeitar' } }
})

// Função auxiliar para salvar estado no localStorage
const saveStateToLocalStorage = (projectId, key, data) => {
  try {
    if (process.client) {
      localStorage.setItem(`voting_${projectId}_${key}`, JSON.stringify(data))
    }
  } catch (error) {
    console.error(`Erro ao salvar ${key} no localStorage:`, error)
  }
}

// Função auxiliar para obter estado do localStorage
const getStateFromLocalStorage = (projectId, key, defaultValue) => {
  try {
    if (process.client) {
      const data = localStorage.getItem(`voting_${projectId}_${key}`)
      return data ? JSON.parse(data) : defaultValue
    }
  } catch (error) {
    console.error(`Erro ao obter ${key} do localStorage:`, error)
  }
  return defaultValue
}

export const mutations = {
  SET_ACTIVE_VOTING(state, { projectId, voting }) {
    state.activeVoting = voting
    saveStateToLocalStorage(projectId, 'activeVoting', voting)
  },
  ADD_PAST_VOTING(state, { projectId, voting }) {
    state.pastVotings.push(voting)
    saveStateToLocalStorage(projectId, 'pastVotings', state.pastVotings)
  },
  SET_ANNOTATION_RULES(state, { projectId, rules }) {
    state.annotationRules = rules
    saveStateToLocalStorage(projectId, 'annotationRules', rules)
  },
  ADD_ANNOTATION_RULE(state, { projectId, rule }) {
    state.annotationRules.push(rule)
    saveStateToLocalStorage(projectId, 'annotationRules', state.annotationRules)
  },
  ADD_VOTE(state, { projectId, ruleId, vote, userId }) {
    // Inicializar votos para esta regra se não existirem
    if (!state.votes[ruleId]) {
      state.votes[ruleId] = {}
    }
    
    // Registrar voto do usuário para esta regra
    state.votes[ruleId][userId] = vote
    
    // Persistir os votos no localStorage
    saveStateToLocalStorage(projectId, 'votes', state.votes)
  },
  // Nova mutation para definir o estado completo dos votos
  SET_VOTES(state, votes) {
    state.votes = votes
  },
  // Nova mutation para definir o estado completo de votações passadas
  SET_PAST_VOTINGS(state, pastVotings) {
    state.pastVotings = pastVotings
  }
}

export const actions = {
  // Inicializar estado de votação para um projeto
  initVotingState({ commit }, projectId) {
    try {
      // Carregar dados do localStorage específicos do projeto
      const savedRules = getStateFromLocalStorage(projectId, 'annotationRules', [])
      const savedActiveVoting = getStateFromLocalStorage(projectId, 'activeVoting', null)
      const savedPastVotings = getStateFromLocalStorage(projectId, 'pastVotings', [])
      const savedVotes = getStateFromLocalStorage(projectId, 'votes', {})
      
      // Restaurar estado da aplicação
      commit('SET_ANNOTATION_RULES', { projectId, rules: savedRules })
      commit('SET_ACTIVE_VOTING', { projectId, voting: savedActiveVoting })
      commit('SET_PAST_VOTINGS', savedPastVotings)
      commit('SET_VOTES', savedVotes)
      
      // Se não houver regras salvas, iniciar com uma lista vazia
      if (savedRules.length === 0) {
        commit('SET_ANNOTATION_RULES', { projectId, rules: [] })
      }
      
      return { success: true }
    } catch (error) {
      console.error('Erro ao inicializar estado de votação:', error)
      return { success: false, error }
    }
  },

  // Criar uma nova regra de anotação
  createAnnotationRule({ commit }, { projectId, rule }) {
    try {
      // TODO: Enviar para API real
      
      // Para desenvolvimento, gerar ID único
      const ruleId = Date.now()
      
      // Criar objeto de regra com ID gerado
      const newRule = {
        id: ruleId,
        ...rule
      }
      
      // Adicionar a regra ao estado
      commit('ADD_ANNOTATION_RULE', { projectId, rule: newRule })
      
      return { success: true, data: newRule }
    } catch (error) {
      console.error('Erro ao criar regra de anotação:', error)
      return { success: false, error }
    }
  },

  // Criar nova votação
  createVoting({ commit, state }, { projectId, votingData }) {
    try {
      // TODO: Enviar para API real
      
      // Para desenvolvimento, gerar ID único
      const votingId = Date.now()
      
      // Criar objeto de votação com ID gerado
      const newVoting = {
        id: votingId,
        projectId, // Armazenar o ID do projeto na votação
        ...votingData
      }
      
      // Se já existir uma votação ativa, mover para histórico
      if (state.activeVoting) {
        commit('ADD_PAST_VOTING', { projectId, voting: state.activeVoting })
      }
      
      // Definir nova votação como ativa
      commit('SET_ACTIVE_VOTING', { projectId, voting: newVoting })
      
      return { success: true, data: newVoting }
    } catch (error) {
      console.error('Erro ao criar votação:', error)
      return { success: false, error }
    }
  },
  
  // Finalizar votação antecipadamente
  endVotingEarly({ commit, state }, { projectId }) {
    try {
      if (!state.activeVoting) {
        throw new Error('Não há votação ativa para finalizar')
      }
      
      // Obter votação atual
      const currentVoting = { ...state.activeVoting }
      
      // Atualizar a data de término para a data atual
      currentVoting.endDate = new Date().toISOString()
      currentVoting.endedEarly = true
      
      // Adicionar ao histórico de votações
      commit('ADD_PAST_VOTING', { projectId, voting: currentVoting })
      
      // Limpar a votação ativa
      commit('SET_ACTIVE_VOTING', { projectId, voting: null })
      
      return { success: true, data: currentVoting }
    } catch (error) {
      console.error('Erro ao finalizar votação:', error)
      return { success: false, error }
    }
  },
  
  // Registrar voto em uma regra
  voteForRule({ commit, rootGetters, state }, { ruleId, vote }) {
    try {
      // Obter ID do usuário atual
      const userId = rootGetters['auth/getUserId']
      
      if (!userId) {
        throw new Error('Usuário não autenticado')
      }
      
      // Obter o ID do projeto da votação ativa
      const projectId = state.activeVoting.projectId
      
      // Registrar voto no estado
      commit('ADD_VOTE', { projectId, ruleId, vote, userId })
      
      return { success: true }
    } catch (error) {
      console.error('Erro ao registrar voto:', error)
      return { success: false, error }
    }
  }
}

export const getters = {
  activeVoting: state => state.activeVoting,
  
  // Filtrar votações passadas pelo ID do projeto
  pastVotings: (state) => (projectId) => {
    return state.pastVotings.filter(voting => {
      // Verificar se a votação tem um projectId definido
      // e se esse projectId corresponde ao projeto atual
      return voting && voting.projectId === projectId;
    });
  },
  
  annotationRules: state => state.annotationRules,
  hasActiveVoting: state => !!state.activeVoting,
  
  // Retorna os votos para uma regra
  ruleVotes: state => ruleId => {
    const votes = { aprovar: 0, rejeitar: 0 }
    
    // Se não existirem votos para esta regra, retorna contagem zerada
    if (!state.votes[ruleId]) {
      return votes
    }
    
    // Conta os votos para cada opção
    Object.values(state.votes[ruleId]).forEach(vote => {
      if (vote === 'aprovar' || vote === 'rejeitar') {
        votes[vote]++
      }
    })
    
    return votes
  },
  
  // Verifica se um usuário votou em uma regra específica
  hasUserVotedForRule: (state, _getters, _rootState, rootGetters) => ruleId => {
    const userId = rootGetters['auth/getUserId']
    
    if (!userId || !state.votes[ruleId]) {
      return false
    }
    
    return !!state.votes[ruleId][userId]
  },
  
  // Obtém o voto de um usuário para uma regra específica
  getUserVoteForRule: (state, _getters, _rootState, rootGetters) => ruleId => {
    const userId = rootGetters['auth/getUserId']
    
    if (!userId || !state.votes[ruleId]) {
      return null
    }
    
    return state.votes[ruleId][userId]
  }
} 