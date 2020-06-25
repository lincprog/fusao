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
  component: () => import('../views/Home')
},
{
  path: '/auth',
  name: 'Auth',
  component: () => import('../views/Auth')
},
{
  path: '/empresa',
  name: 'Empresa',
  component: () => import('../views/Empresa')
},
{
  path: '/fusao',
  name: 'fusao',
  component: () => import('../views/Fusao')
}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach(beforeEach)

export default router
