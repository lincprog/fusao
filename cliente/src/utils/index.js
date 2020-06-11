import { get } from 'lodash'

export const getData = obj => get(obj, 'data')

export const getError = (e) => {
  let erro
  if (e && e.response && e.response.data) {
    // Vue.toasted.global.defaultError({ msg: e.response.data })
    erro = e.response.data
  } else if (typeof e === 'string') {
    // Vue.toasted.global.defaultError({ msg: e })
    erro = e
  } else {
    // Vue.toasted.global.defaultError()
    erro = 'Oops.. Erro inesperado.'
  }
  return erro
}
