import Vue from 'vue'
import Vuex from 'vuex'
import { isEmpty } from 'lodash'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {},
    token: null,
    isMenuVisible: false,
    messages: {
      success: 'Sucesso',
      error: ['Erro', 'Tambem'],
      warning: 'cuidado',
      validation: ['nao passou', 'tente novamente', 'agora vai']
    },
    fetching: true
  },
  mutations: {
    'Auth/SET_TOKEN' (state, value) {
      state.token = value
    },
    'Auth/SET_USER' (state, value) {
      state.user = value
    },
    'MAIN_SET_FETCHING' (state, obj) {
      state.fetching = obj.fetching
    },
    'MAIN_SET_MESSAGE' (state, obj) {
      state.messages[obj.type] = obj.message
    },
    setUser (state, user) {
      state.user = user
      if (user) {
        // axios.defaults.headers.common.Authorization = `bearer ${user.token}`
        state.isMenuVisible = true
      } else {
        // delete axios.defaults.headers.common.Authorization
        state.isMenuVisible = false
      }
    },
    toggleMenu (state, isVisible) {
      if (!state.user) {
        state.isMenuVisible = false
        return
      }

      if (isVisible === undefined) {
        state.isMenuVisible = !state.isMenuVisible
      } else {
        state.isMenuVisible = isVisible
      }
    }
  },
  actions: {
    setFetching ({ commit }, obj) {
      commit('MAIN_SET_FETCHING', obj)
    },
    setMessage ({ commit }, obj) {
      commit('MAIN_SET_MESSAGE', obj)
    },
    resetMessages ({ commit }) {
      commit('MAIN_SET_MESSAGE', { type: 'success', message: '' })
      commit('MAIN_SET_MESSAGE', { type: 'error', message: [] })
      commit('MAIN_SET_MESSAGE', { type: 'warning', message: '' })
      commit('MAIN_SET_MESSAGE', { type: 'validation', message: [] })
    }
  },
  modules: {
  },
  getters: {
    isLogged: ({ token }) => !isEmpty(token),
    currentUser: ({ user }) => user,
    isAuthPage: ({ route }) => route.path.indexOf('/auth') !== -1,
    shouldShowNavigation: ({ route }, getters) => (route.path ? !getters.isAuthPage : false)
  }
})
