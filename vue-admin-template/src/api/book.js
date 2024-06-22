import request from '@/utils/request'

// 获得所有书目信息
export function getAllBooks() {
  return request({
    url: 'http://127.0.0.1:8000/api/get-all-books/',
    method: 'get'
  })
}

// 添加新书目
export function addBookInfo(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/book-info/',
    method: 'post',
    data
  })
}

// 添加索书号对应图书
export function addBook(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/book/',
    method: 'post',
    data
  })
}

// 删除书目
export function deleteBookInfo(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/delete-book-info/',
    method: 'delete',
    data
  })
}

// 删除索书号对应图书
export function deleteBook(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/delete-book/',
    method: 'delete',
    data
  })
}

// 修改书目信息
export function updateBookInfo(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/update-book-info/',
    method: 'post',
    data
  })
}

// 修改索书号对应图书馆藏位置
export function updateBookLocation(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/update-book-location/',
    method: 'post',
    data
  })
}

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
