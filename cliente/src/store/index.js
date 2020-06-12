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
    messages: {
      success: '',
      error: [],
      warning: '',
      validation: []
    },
    fetching: false
  },
  mutations: {
    setToken (state, value) {
      state.token = value
    },
    setUser2 (state, value) {
      state.user = value
    },
    setFetching (state, obj) {
      state.fetching = obj.fetching
    },
    setMessage (state, obj) {
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
    registerUser ({ dispatch }, payload) {
      return services.postRegister(payload)
        .then(res => res)
    },
    attemptLogin ({ dispatch }, payload) {
      return services.postLogin(payload)
        .then(user => {
          localStorage.setItem(userKey, JSON.stringify(user))
          console.log(user)
          const { name, email, token } = user
          dispatch('setUser', { name, email })
          dispatch('setToken', token)
          return user // keep promise chain
        })
    },
    setFetching ({ commit }, obj) {
      commit('setFetching', obj)
    },
    setMessage ({ commit }, obj) {
      commit('setMessage', obj)
    },
    resetMessages ({ commit }) {
      commit('setMessage', { type: 'success', message: '' })
      commit('setMessage', { type: 'error', message: [] })
      commit('setMessage', { type: 'warning', message: '' })
      commit('setMessage', { type: 'validation', message: [] })
    },
    checkUserToken: ({ dispatch, state }) => {
      if (!isEmpty(state.token)) {
        return Promise.resolve(state.token)
      }
      const json = localStorage.getItem(userKey)
      const user = JSON.parse(json)
      console.log(user)
      if (isEmpty(user) || isEmpty(user.token)) {
        return Promise.reject(new Error('NO_TOKEN'))
      }
      const { name, email, token } = user
      dispatch('setUser', { name, email })
      return dispatch('setToken', token)
    },
    setToken: ({ commit }, payload) => {
      const token = (isEmpty(payload)) ? null : payload.token || payload
      httpSetToken(token)
      commit('setToken', token)
      return Promise.resolve(token) // keep promise chain
    },
    setUser: ({ commit }, user) => {
      commit('setUser', user)
      Promise.resolve(user) // keep promise chain
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

// const subscribe = (store) => {
//   store.subscribe((mutation, { Auth }) => {
//     if (TYPES.SET_TOKEN === mutation.type) {
//       /**
//        * Set the Axios Authorization header with the token
//        */
//       httpSetToken(Auth.token)

//       /**
//        * Sets the token to the local storage
//        * for auto-login purpose
//        */
//       localforage.setItem(userTokenStorageKey, Auth.token)
//     }
//   })
// }

// export default (store) => {
//   subscribe(store)
// };
