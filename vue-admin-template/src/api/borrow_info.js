import request from '@/utils/request'

// 获取所有借阅信息
export function getAllBorrowInfo() {
  return request({
    url: 'http://127.0.0.1:8000/api/get-all-borrowing-info/',
    method: 'get'
  })
}

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
