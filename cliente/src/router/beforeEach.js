import store from '../store'

const needAuth = auth => auth === true
const beforeEach = (to, from, next) => {
  const auth = to.meta.requiresAuth
  store.dispatch('resetMessages')
  if (!needAuth(auth)) {
    next()
  } else {
    store.dispatch('checkUserToken')
      .then(() => next())
      .catch(() => next({ path: '/auth' }))
  }
}

export default beforeEach
