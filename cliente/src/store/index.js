import Vue from 'vue'
import Vuex from 'vuex'
import { isEmpty } from 'lodash'
import { userKey } from '../config'
import * as services from '../services'
import { setToken as httpSetToken } from '../plugins/http'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {},
    token: null,
    isMenuVisible: false,
    alert: { type: '', message: '' },
    loading: false
  },
  mutations: {
    setToken (state, value) {
      state.token = value
    },
    setLoading (state, { loading }) {
      state.loading = loading
    },
    setAlert (state, obj) {
      state.alert = obj
    },
    setUser (state, obj) {
      state.user = obj
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
    setSuccess ({ commit }, { message }) {
      commit('setAlert', { type: 'success', message })
    },
    setWarning ({ commit }, { message }) {
      commit('setAlert', { type: 'warning', message })
    },
    setInfo ({ commit }, { message }) {
      commit('setAlert', { type: 'info', message })
    },
    setError ({ commit }, { message }) {
      commit('setAlert', { type: 'error', message })
    },
    clearAlert ({ commit }) {
      commit('setAlert', { type: '', message: '' })
    },
    registerUser ({ dispatch }, payload) {
      return services.postRegister(payload)
        .then(res => res)
    },
    attemptLogin ({ dispatch, commit }, payload) {
      return services.postLogin(payload)
        .then(user => {
          localStorage.setItem(userKey, JSON.stringify(user))
          const { name, email, token } = user
          commit('setUser', { name, email })
          dispatch('setToken', token)
          return user
        })
    },
    setLoading ({ commit }, { loading }) {
      commit('setLoading', { loading })
    },
    checkUserToken: ({ dispatch, commit, state }) => {
      if (!isEmpty(state.token)) {
        return Promise.resolve(state.token)
      }
      const json = localStorage.getItem(userKey)
      const user = JSON.parse(json)
      if (isEmpty(user) || isEmpty(user.token)) {
        return Promise.reject(new Error('NO_TOKEN'))
      }
      const { name, email, token } = user
      commit('setUser', { name, email })
      dispatch('setToken', token)
      return Promise.resolve(state.token)
    },
    setToken: ({ commit }, payload) => {
      const token = (isEmpty(payload)) ? null : payload.token
      httpSetToken(token)
      commit('setToken', token)
    }
  },
  modules: {
  },
  getters: {
    isLogged: ({ token }) => !isEmpty(token),
    currentUser: ({ user }) => user
    // isAuthPage: ({ route }) => route.path.indexOf('/auth') !== -1,
    // shouldShowNavigation: ({ route }, getters) => (route.path ? !getters.isAuthPage : false)
  }
})
