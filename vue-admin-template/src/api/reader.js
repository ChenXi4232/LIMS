import request from '@/utils/request'

// 查询读者
export function findReader(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/search-reader/',
    method: 'post',
    data
  })
}

// 查询读者类型
export function findReaderType(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/search-reader-type/',
    method: 'post',
    data
  })
}

// 更新读者信息
export function updateReader(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/update-reader/',
    method: 'post',
    data
  })
}

// 更新读者类型信息，学生
export function updateStudentType(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/update-reader-student/',
    method: 'post',
    data
  })
}

// 更新读者类型信息，教职工
export function updateFacultyType(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/update-reader-faculty/',
    method: 'post',
    data
  })
}
