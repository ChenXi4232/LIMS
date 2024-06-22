import request from '@/utils/request'

// 创建读者
export function createReader(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/reader/',
    method: 'post',
    data
  })
}

// 注销
export function deleteReader(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/delete-reader/',
    method: 'delete',
    data
  })
}

// 查询读者
export function findReader(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/search-reader/',
    method: 'post',
    data
  })
}

// 返回所有读者
export function getAllReader() {
  return request({
    url: 'http://127.0.0.1:8000/api/get-all-reader/',
    method: 'get'
  })
}

// 添加学生类型
export function addStudentType(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/reader-student/',
    method: 'post',
    data
  })
}

// 添加教职工类型
export function addFacultyType(data) {
  return request({
    url: 'http://127.0.0.1:8000/api/reader-faculty/',
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
