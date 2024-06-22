import request from '@/utils/request'

// 查找指定借书记录
export function findReservationInfo(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/search-reservation-info/',
    method: 'post',
    data
  })
}

// 取消预约
export function cancelReservation(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/cancel-reservation/',
    method: 'delete',
    data
  })
}
