import axios from 'axios'

export const http = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 10_000,
})