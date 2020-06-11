import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home'

Vue.use(VueRouter)

const routes = [{
  path: '*',
  redirect: '/'
},
{
  path: '/',
  name: 'Home',
  component: Home
},
{
  path: '/empresa',
  name: 'Empresa',
  component: () => import('../views/Empresa')
},
{
  path: '/auth',
  name: 'Auth',
  component: () => import('../views/Auth')
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

export default router
