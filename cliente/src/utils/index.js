import { get, isArray } from 'lodash'

export const getData = obj => get(obj, 'data')

export const getMessageError = obj => {
  let msg = ''
  if (typeof obj === 'string') {
    msg = obj
  } else if (isArray(obj)) {
    msg = obj.join(',')
  } else if (typeof obj === 'object') {
    for (const key in obj) {
      msg += `${key}: ${obj[key]}`
    }
  } else {
    msg = 'Oops.. Erro inesperado.'
  }
  return msg
}
