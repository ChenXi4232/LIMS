import request from '@/utils/request'

export function bookSearch(data) {
  // console.log('test', data)
  return request({
    url: 'http://127.0.0.1:8000/api/search-book/',
    method: 'post',
    data
  })
}

// 获得每样书的所有样本信息
export function getBooksByCall(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/get-books-by-call-number/',
    method: 'post',
    data
  })
}

// 获得所有书目信息
export function getAllBooks() {
  return request({
    url: 'http://127.0.0.1:8000/api/get-all-books/',
    method: 'get'
  })
}

// 借书
export function borrowBook(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/borrowing-info/',
    method: 'post',
    data
  })
}

// 预约
export function reserveBook(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/reservation-info/',
    method: 'post',
    data
  })
}

// 还书
export function returnBook(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/reservation-info/',
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
