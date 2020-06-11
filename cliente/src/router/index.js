import Vue from 'vue'
import VueRouter from 'vue-router'
import { userKey } from '../config'

Vue.use(VueRouter)

const routes = [{
  path: '*',
  redirect: '/'
},
{
  path: '/',
  name: 'Home',
  component: () => import('../views/Home'),
  meta: { requiresAuth: true }
},
{
  path: '/empresa',
  name: 'Empresa',
  component: () => import('../views/Empresa'),
  meta: { requiresAuth: true }
},
{
  path: '/auth',
  name: 'Auth',
  component: () => import('../views/Auth'),
  meta: { requiresAuth: false }
},
{
  path: '/fusao',
  name: 'fusao',
  component: () => import('../views/Fusao'),
  meta: { requiresAuth: true }
}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  console.log('antes das rotas ->', userKey)
  // const json = localStorage.getItem(userKey)
  // if (to.matched.some(record => record.meta.requiresAdmin)) {
  //   const user = JSON.parse(json)
  //   user && user.admin ? next() : next({ path: '/' })
  // } else {
  //   next()
  // }
})
const needAuth = auth => auth === true
const beforeEach = (to, from, next) => {
  const auth = to.meta.requiresAuth
  /**
  * Clears all global feedback message
  * that might be visible
  */
  // store.dispatch('resetMessages')
  /**
   * If route doesn't require authentication be normally accessed.
   */
  if (!needAuth(auth)) {
    next()
    // return to prevent the code from continuing in its flow
    // With this flow `else` or `else if` is not necessary
  }

  /**
   * Otherwise  if authentication is required login.
   */
  // store.dispatch('checkUserToken')
  //   .then(() => {
  //     // There is a token and it is valid
  //     next() // can access the route
  //   })
  //   .catch(() => {
  //     // No token, or it is invalid
  //     next({ name: 'auth.signin' }) // redirect to login
  //   })
}
console.log('beforeeach', beforeEach)

export default router
