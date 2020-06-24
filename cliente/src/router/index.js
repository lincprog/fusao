import Vue from 'vue'
import VueRouter from 'vue-router'
import beforeEach from './beforeEach'

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

router.beforeEach(beforeEach)

export default router
