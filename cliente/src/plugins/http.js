import axios from 'axios'
import { baseApiUrl } from '../config'

export const http = axios.create({
  baseURL: baseApiUrl
})
