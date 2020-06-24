import store from '../store'

const needAuth = auth => auth === true
const beforeEach = (to, from, next) => {
  const auth = to.meta.requiresAuth
  console.log('to', to, 'from', from)
  if (!needAuth(auth)) {
    next()
    return
  }
  store.dispatch('checkUserToken')
    .then(() => next())
    .catch(() => next({ name: 'Auth' }))
}

export default beforeEach
