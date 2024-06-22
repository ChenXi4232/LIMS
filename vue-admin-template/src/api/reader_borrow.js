import request from '@/utils/request'

// 还书
export function returnBook(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/return-book/',
    method: 'post',
    data
  })
}

// 查找指定借书记录
export function findBorrowInfo(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/search-borrowing-info/',
    method: 'post',
    data
  })
}

// 续借
export function renewBook(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/renew-book/',
    method: 'post',
    data
  })
}
