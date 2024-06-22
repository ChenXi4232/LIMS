<template>
  <div class="app-container">

    <el-form ref="list" :model="list" label-width="100px">
      <el-form-item label="姓名" prop="name">
        {{ list.name }}
      </el-form-item>
      <el-form-item label="读者证 ID" prop="reader_card_id">
        {{ list.reader_card_id }}
      </el-form-item>
      <el-form-item label="地址" prop="address">
        {{ list.address }}
      </el-form-item>
      <el-form-item label="联系电话" prop="phone_number">
        {{ list.phone_number }}
      </el-form-item>
      <el-form-item label="电子邮件" prop="email">
        {{ list.email }}
      </el-form-item>
      <el-form-item label="性别" prop="gender">
        {{ list.gender }}
      </el-form-item>
      <el-form-item label="有效期" prop="expiration_date">
        {{ list.expiration_date }}
      </el-form-item>
      <el-form-item label="读者证照片">
        <img v-if="list.reader_card_photo" :src="'http://127.0.0.1:8000/' + list.reader_card_photo" alt="预览图片" style="max-width: 200px; max-height: 200px;">
        <span v-else>暂无图片</span>
      </el-form-item>
      <el-form-item label="出生日期" prop="date_of_birth">
        {{ list.date_of_birth }}
      </el-form-item>
      <el-form-item label="借阅限额" prop="borrowing_limit">
        {{ list.borrowing_limit }}
      </el-form-item>
    </el-form>

    <el-form ref="listType" v-if="dialogVisibleAddReaderTypeS" :model="listType" label-width="100px">
      <el-form-item label="读者证 ID" prop="reader_card_id">
        {{ listType.reader_card_id }}
      </el-form-item>
      <el-form-item label="专业" prop="major">
        {{ listType.major }}
      </el-form-item>
      <el-form-item label="学号" prop="student_id">
        {{ listType.student_id }}
      </el-form-item>
    </el-form>

    <el-form ref="listType" v-if="dialogVisibleAddReaderTypeF" :model="listType" label-width="100px">
      <el-form-item label="读者证 ID" prop="reader_card_id">
        {{ listType.reader_card_id }}
      </el-form-item>
      <el-form-item label="部门" prop="department">
        {{ listType.department }}
      </el-form-item>
      <el-form-item label="教工号" prop="faculty_id">
        {{ listType.faculty_id }}
      </el-form-item>
    </el-form>

    <el-dialog
      title="修改读者"
      :visible.sync="dialogVisibleAddReader"
      width="70%"
      center
    >
      <el-form ref="listAdd" :model="listAdd" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="listAdd.name" placeholder="请输入姓名" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item label="读者证 ID" prop="reader_card_id">
          <el-input v-model="listAdd.reader_card_id" placeholder="请输入读者证 ID" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="listAdd.address" placeholder="请输入地址" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone_number">
          <el-input v-model="listAdd.phone_number" placeholder="请输入联系电话" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item label="电子邮件" prop="email">
          <el-input v-model="listAdd.email" placeholder="请输入电子邮件" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-input v-model="listAdd.gender" placeholder="请输入性别" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item label="有效期" prop="expiration_date">
          <el-input v-model="listAdd.expiration_date" placeholder="请输入有效期" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item label="读者证照片" prop="reader_card_photo">
          <el-upload
            :headers="headers"
            action="http://127.0.0.1:8000/api/upload-reader-card-photo/"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            accept="image/jpg,image/jpeg,image/png"
          >
            <el-button size="small" type="primary">点击上传</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="预览图片">
          <img v-if="listAdd.reader_card_photo" :src="'http://127.0.0.1:8000/' + listAdd.reader_card_photo" alt="预览图片" style="max-width: 200px; max-height: 200px;">
          <span v-else>暂无图片</span>
        </el-form-item>
        <el-form-item label="出生日期" prop="date_of_birth">
          <el-input v-model="listAdd.date_of_birth" placeholder="请输入出生日期" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item label="借阅限额" prop="borrowing_limit">
          <el-input v-model="listAdd.borrowing_limit" placeholder="请输入借阅限额" clearable @clear="handleClearAdd" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addReaderInfo">添加</el-button>
          <el-button @click="dialogVisibleAddReader = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog
      title="添加学生读者"
      :visible.sync="dialogVisibleAddReaderTypeS"
      width="70%"
      center
    >
      <el-form ref="listAddStudentType" :model="listAddStudentType" label-width="100px">
        <el-form-item label="读者证 ID" prop="reader_card_id">
          <el-input v-model="listAddStudentType.reader_card_id" placeholder="请输入读者证 ID" clearable @clear="handleClearAddStudentType" />
        </el-form-item>
        <el-form-item label="专业" prop="major">
          <el-input v-model="listAddStudentType.major" placeholder="请输入专业" clearable @clear="handleClearAddStudentType" />
        </el-form-item>
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="listAddStudentType.student_id" placeholder="请输入学号" clearable @clear="handleClearAddStudentType" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addStudentType">添加</el-button>
          <el-button @click="dialogVisibleAddReaderTypeS = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog
      title="添加教职工读者"
      :visible.sync="dialogVisibleAddReaderTypeF"
      width="70%"
      center
    >
      <el-form ref="listAddFacultyType" :model="listAddFacultyType" label-width="100px">
        <el-form-item label="读者证 ID" prop="reader_card_id">
          <el-input v-model="listAddFacultyType.reader_card_id" placeholder="请输入读者证 ID" clearable @clear="handleClearAddFacultyType" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="listAddFacultyType.department" placeholder="请输入部门" clearable @clear="handleClearAddFacultyType" />
        </el-form-item>
        <el-form-item label="教工号" prop="faculty_id">
          <el-input v-model="listAddFacultyType.faculty_id" placeholder="请输入教工号" clearable @clear="handleClearAddFacultyType" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addFacultyType">添加</el-button>
          <el-button @click="dialogVisibleAddReaderTypeF = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>

<script>
import { createReader, deleteReader, findReader, getAllReader, addFacultyType, addStudentType, findReaderType } from '@/api/reader_info'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination'
import user from '@/store'
import { getToken } from '@/utils/auth'

export default {
  name: 'ReaderInfo',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      list: [],
      listType: [],
      total: 0,
      imageUrl: '',
      dialogVisible: false,
      dialogVisibleAddReader: false,
      dialogVisibleTypeS: false,
      dialogVisibleTypeF: false,
      dialogVisibleDeleteReaderInfo: false,
      dialogVisibleImage: false,
      dialogVisibleBook: false,
      dialogVisibleAddReaderTypeS: false,
      dialogVisibleAddReaderTypeF: false,
      dialogVisibleBorrowBook: false,
      dialogVisibleReserveBook: false,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        reader_card_id: undefined,
        name: undefined,
        phone_number: undefined,
        gender: undefined,
        sort: '+name'
      },
      listAdd: {
        reader_card_id: '',
        name: '',
        phone_number: '',
        email: '',
        gender: '',
        registration_date: '',
        expiration_date: '',
        borrowing_limit: '',
        reader_card_photo: '',
        date_of_birth: '',
        outstanding_amount: '',
        borrowing_count: '',
        address: ''
      },
      listAddStudentType: {
        reader_card_id: '',
        major: '',
        student_id: ''
      },
      listAddFacultyType: {
        reader_card_id: '',
        department: '',
        faculty_id: ''
      },
      listDistribution: [],
      searchText: '', // 用户输入的搜索关键字
      searchLoading: false, // 搜索加载状态
      bookID: undefined,
      readerCardID: undefined,
      name: '',
      callNumber: undefined,
      deleteReaderCardID: undefined,
      readerType: undefined
    }
  },
  computed: {
    headers() {
      return {
        Authorization: 'Bearer ' + getToken()
      }
    }
  },
  // mounted() {
  //   this.fetchData()
  //   this.handleCollectionDistribution()
  // },
  created() {
    this.fetchData()
    this.getUserInfo()
  },
  methods: {
    // 查询读者类型信息
    lookUpType(readerCardID) {
      findReaderType({ reader_card_id: readerCardID }).then(response => {
        this.listType = response.data.info
        if (this.listType.type === 'student') {
          this.dialogVisibleTypeS = true
        } else {
          this.dialogVisibleTypeF = true
        }
      }).catch(error => {
        console.error('查询失败', error)
      })
    },
    // 根据文本框输入内容判断读者类型
    handleReaderType() {
      if (this.readerType === '教职工') {
        this.dialogVisibleAddReaderTypeF = true
      } else if (this.readerType === '学生') {
        this.dialogVisibleAddReaderTypeS = true
      } else {
        this.$message.error('请输入正确的读者类型')
      }
    },
    // 添加学生类型
    addStudentType() {
      this.$refs['listAddStudentType'].validate((valid) => {
        if (valid) {
          const readerInfoData = {
            reader_card_id: this.listAddStudentType.reader_card_id,
            major: this.listAddStudentType.major,
            student_id: this.listAddStudentType.student_id
          }
          addStudentType(readerInfoData).then(response => {
            this.$message({
              message: '添加成功',
              type: 'success'
            })
            this.dialogVisibleAddReaderTypeS = false
          }).catch(error => {
            console.error('添加失败', error)
            this.dialogVisibleAddReaderTypeS = false
          })
        }
      })
    },
    // 添加教师类型
    addFacultyType() {
      this.$refs['listAddFacultyType'].validate((valid) => {
        if (valid) {
          const readerInfoData = {
            reader_card_id: this.listAddFacultyType.reader_card_id,
            department: this.listAddFacultyType.department,
            faculty_id: this.listAddFacultyType.faculty_id
          }
          addFacultyType(readerInfoData).then(response => {
            this.$message({
              message: '添加成功',
              type: 'success'
            })
            this.dialogVisibleAddReaderTypeF = false
          }).catch(error => {
            console.error('添加失败', error)
            this.dialogVisibleAddReaderTypeF = false
          })
        }
      })
    },
    // 删除图书信息按钮
    deleteReaderButton(row) {
      this.dialogVisibleDeleteReaderInfo = true
      this.deleteReaderCardID = row.reader_card_id
    },
    // 删除图书信息
    deleteReaderInfo() {
      // console.log(this.deleteCallNumber)
      const deleteBookInfoData = {
        reader_card_id: this.deleteReaderCardID
      }
      deleteReader(deleteBookInfoData).then(response => {
        this.$message({
          message: '删除成功',
          type: 'success'
        })
        this.dialogVisibleDeleteReaderInfo = false
        this.handleClearDeleteReader()
        this.fetchData()
      }).catch(error => {
        console.error('删除失败', error)
        this.dialogVisibleDeleteReaderInfo = false
        this.handleClearDeleteReader()
      })
    },
    handleClearDeleteReader() {
      this.deleteReaderCardID = undefined
    },
    handleUploadSuccess(response) {
      if (response['code'] === 20000) {
        this.listAdd.reader_card_photo = response.data.image_url
        // console.log('上传成功', response.data.image_url)
        // console.log(this.listAdd.reader_card_photo)
        this.$message({
          message: '上传成功',
          type: 'success'
        })
      } else {
        this.$message.error('上传失败')
      }
    },
    beforeUpload(file) {
      // 限制大小 2MB
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('上传封面图片大小不能超过 2MB!')
      }
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/jpg'
      if (!isJPG) {
        this.$message.error('上传封面图片只能是 JPG 或 PNG 格式!')
      }
      return isJPG && isLt2M
    },
    addReaderInfo() {
      this.$refs['listAdd'].validate((valid) => {
        if (valid) {
          const readerInfoData = {
            reader_card_id: this.listAdd.reader_card_id,
            name: this.listAdd.name,
            phone_number: this.listAdd.phone_number,
            email: this.listAdd.email,
            gender: this.listAdd.gender,
            expiration_date: this.listAdd.expiration_date,
            borrowing_limit: this.listAdd.borrowing_limit,
            reader_card_photo: this.listAdd.reader_card_photo,
            date_of_birth: this.listAdd.date_of_birth,
            address: this.listAdd.address
          }
          createReader(readerInfoData).then(response => {
            this.$message({
              message: '添加成功',
              type: 'success'
            })
            this.dialogVisibleAddReader = false
            this.fetchData()
          }).catch(error => {
            console.error('添加失败', error)
            this.dialogVisibleAddReader = false
          })
        }
      })
    },
    handleSearch() {
      if (this.listQuery.name === undefined) {
        this.listQuery.name = ''
      }
      if (this.listQuery.reader_card_id === undefined) {
        this.listQuery.reader_card_id = ''
      }
      if (this.listQuery.phone_number === undefined) {
        this.listQuery.phone_number = ''
      }
      if (this.listQuery.gender === undefined) {
        this.listQuery.gender = ''
      }
      this.searchLoading = true
      findReader(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.dialogVisible = true
        this.searchLoading = false
        this.$message({
          message: '读者记录搜索完成',
          type: 'success'
        })
      }).catch(error => {
        console.error('读者记录搜索失败', error)
        this.searchLoading = false
      })
    },
    handleClear() {
      this.listQuery.gender = undefined
      this.listQuery.reader_card_id = undefined
      this.listQuery.name = undefined
      this.listQuery.phone_number = undefined
    },
    handleClearAdd() {
      this.listAdd.reader_card_id = ''
      this.listAdd.name = ''
      this.listAdd.phone_number = ''
      this.listAdd.email = ''
      this.listAdd.borrowing_limit = ''
      this.listAdd.date_of_birth = ''
      this.listAdd.registration_date = ''
      this.listAdd.reader_card_photo = ''
      this.listAdd.gender = ''
      this.listAdd.address = ''
    },
    handleClearAddStudentType() {
      this.listAddStudentType.reader_card_id = ''
      this.listAddStudentType.major = ''
      this.listAddStudentType.student_id = ''
    },
    handleClearAddFacultyType() {
      this.listAddFacultyType.reader_card_id = ''
      this.listAddFacultyType.department = ''
      this.listAddFacultyType.faculty_id = ''
    },
    getUserInfo() {
      this.name = user.getters.name
    },
    fetchData() {
      this.listLoading = true
      getAllReader().then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.dialogVisible = true
        this.listLoading = false
        this.$message({
          message: '读者记录查询完成',
          type: 'success'
        })
      }).catch(error => {
        console.error('读者记录查询失败', error)
        this.listLoading = false
      })
    },
    showFile(filePath) {
      // 设置要显示的图片路径
      this.imageUrl = 'http://127.0.0.1:8000/' + filePath
      // 打开 Dialog
      this.dialogVisibleImage = true
    }
  }
}
</script>
