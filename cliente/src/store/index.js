import Vue from 'vue'
import Vuex from 'vuex'
import { userKey } from '../config'
import * as services from '../services'
import { setToken as httpSetToken, deleteToken } from '../plugins/http'

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
    setToken: (state, value) => {
      state.token = value
    },
    setLoading: (state, { loading }) => {
      state.loading = loading
    },
    setAlert: (state, obj) => {
      state.alert = obj
    },
    setUser: (state, obj) => {
      state.user = obj
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
    registerUser (payload) {
      return services.postRegister(payload)
        .then(res => res)
    },
    attemptLogin ({ dispatch, commit }, payload) {
      return services.postLogin(payload)
        .then(user => {
          localStorage.setItem(userKey, JSON.stringify(user))
          const { name, email, token } = user
          commit('setUser', { name, email })
          dispatch('storeToken', token)
          return user
        })
    },
    logout ({ commit }) {
      commit('setUser', {})
      commit('setToken', null)
      deleteToken()
      localStorage.removeItem(userKey)
    },
    setLoading ({ commit }, { loading }) {
      commit('setLoading', { loading })
    },
    storeToken ({ commit }, payload) {
      const token = !payload ? null : payload
      httpSetToken(token)
      commit('setToken', token)
    },
    checkUserToken ({ dispatch, commit }) {
      const json = localStorage.getItem(userKey)
      const user = JSON.parse(json)
      if (!user) {
        return Promise.reject(new Error('NO_USER_TOKEN'))
      }
      const { name, email, token } = user
      commit('setUser', { name, email })
      dispatch('storeToken', token)
      return Promise.resolve(user)
    }
  },
  modules: {
  },
  getters: {
    isLogged: ({ token }) => !!token,
    currentUser: ({ user }) => user
  }
})
