import { http } from '../plugins/http'
import { getData } from '../utils'

// send login data and retrive a new token
export const postLogin = ({ email, password }) =>
  http.post('/login', { email, password })
    .then(getData)

export const postRegister = ({ name, email, password, confirmPassword }) =>
  http.post('/signup', { name, email, password, confirmPassword })
    .then(getData)

// get current user's data
export const loadUserData = () => http.get('/me').then(getData)

// revoke current token
export const revokeToken = () => http.post('/auth/token/revoke').then(getData)
