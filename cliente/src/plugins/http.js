import axios from 'axios'
import { baseApiUrl } from '../config'
import store from '../store'
// import router from '../router'
import { getMessageError } from '../utils'

export const http = axios.create({
  baseURL: baseApiUrl
})

export const setToken = token => {
  http.defaults.headers.common.Authorization = `Bearer ${token}`
}

export const deleteToken = () => {
  console.log('deletou token')
  delete http.defaults.headers.common.Authorization
}

const success = res => res
const error = (error) => {
  const { response } = error
  if (response.status === 401) {
    // router.push('/')
  }
  store.dispatch('setError', { message: getMessageError(response.data.message) })
  store.dispatch('setLoading', { loading: false })
  return Promise.reject(error)
}

http.interceptors.response.use(success, error)
