import axios from 'axios'
import { baseApiUrl } from '../config'

export const http = axios.create({
  baseURL: baseApiUrl
})

export function setToken (token) {
  http.defaults.headers.common.Authorization = `Bearer ${token}`
}

const success = res => res
const error = err => {
  console.log('err', err)
  if (err.response.status === 401) {
    window.location = '/'
  } else {
    return Promise.reject(err)
  }
}

http.interceptors.response.use(success, error)

// const error2 = (error) => {
//   const { response } = error
//   /**
//   * If token is either expired, not provided or invalid
//   * then redirect to login. On server side the error
//   * messages can be changed on app/Providers/EventServiceProvider.php
//   */
//   if ([401, 400].indexOf(response.status) > -1) {
//     router.push({ name: 'auth.signin' })
//   }
//   /**
//   * Error messages are sent in arrays
//   */
//   if (isArray(response.data)) {
//     store.dispatch('setMessage', { type: 'error', message: response.data.messages })
//   /**
//   * Laravel generated validation errors are
//   * sent in an object
//   */
//   } else {
//     store.dispatch('setMessage', { type: 'validation', message: response.data })
//   }

//   store.dispatch('setFetching', { fetching: false })

//   return Promise.reject(error)
// }

// console.log(error2)
