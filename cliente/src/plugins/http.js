import axios from 'axios'
import { baseApiUrl } from '../config'
import store from '../store'
import router from '../router'
import { getMessageError } from '../utils'

export const http = axios.create({
  baseURL: baseApiUrl
})

export function setToken (token) {
  http.defaults.headers.common.Authorization = `Bearer ${token}`
}

const success = res => res
const error = (error) => {
  const { response } = error
  if (response.status === 401) {
    console.log(router)
    router.push('/auth')
  }
  store.dispatch('setError', { message: getMessageError(response.data.message) })
  store.dispatch('setLoading', { loading: false })
  console.log('err', response)
  return Promise.reject(error)
}

http.interceptors.response.use(success, error)
