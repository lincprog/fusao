import store from '../store'

const isAuthRoute = route => route.path.indexOf('/auth') !== -1
const isLogged = () => store.getters.isLogged
const beforeEach = (to, from, next) => {
  if (!isAuthRoute(to) && !isLogged()) {
    next('/auth')
  } else {
    next()
  }
}

export default beforeEach
