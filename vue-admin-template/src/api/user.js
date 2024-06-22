import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'http://127.0.0.1:8000/token/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: 'http://127.0.0.1:8000/api/get-user-info/',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    // url: '/vue-admin-template/user/logout',
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
