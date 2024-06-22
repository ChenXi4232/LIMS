import request from '@/utils/request'
// import state from '@/store/modules/user'

export function getAllLateFeeInfo() {
  return request({
    url: 'http://127.0.0.1:8000/api/get-all-late-fee-info/',
    method: 'get'
  })
}

export function findLateFeeInfo(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/search-late-fee-info/',
    method: 'post',
    data
  })
}

export function updateLateFeeInfoStatus(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/update-late-fee-info-status/',
    method: 'post',
    data
  })
}

