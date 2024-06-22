<template>
  <div class="app-container">
    <div class="filter-container">
      <!-- 搜索框和按钮 -->
      <el-input
        v-model="listQuery.title"
        placeholder="书名"
        style="width: 200px;"
        class="filter-item"
        clearable
        @clear="handleClearSearch()"
      />

      <el-input
        v-model="listQuery.publisher"
        placeholder="出版社"
        style="width: 100px;"
        class="filter-item"
        clearable
        @clear="handleClearSearch()"
      />

      <el-input
        v-model="listQuery.call_number"
        placeholder="索书号"
        style="width: 200px;"
        class="filter-item"
        clearable
        @clear="handleClearSearch()"
      />

      <el-button
        type="primary"
        :loading="searchLoading"
        @click="handleSearch()"
      >
        搜索
      </el-button>
    </div>

    <el-button
      type="primary"
      style="margin-bottom: 20px;"
      @click="dialogVisibleAddBookInfo = true"
    >
      添加图书信息
    </el-button>

    <!-- 表格 -->
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="书名">
        <template slot-scope="scope">
          {{ scope.row.title }}
        </template>
      </el-table-column>
      <el-table-column label="出版社">
        <template slot-scope="scope">
          {{ scope.row.publisher }}
        </template>
      </el-table-column>
      <el-table-column label="简介">
        <template slot-scope="scope">
          {{ scope.row.description }}
        </template>
      </el-table-column>
      <el-table-column label="ISBN">
        <template slot-scope="scope">
          {{ scope.row.isbn }}
        </template>
      </el-table-column>
      <el-table-column label="图书封面">
        <template slot-scope="scope">
          <el-button type="text" @click="showFile(scope.row.cover_image_path)">封面预览</el-button>
        </template>
      </el-table-column>
      <el-table-column label="价格">
        <template slot-scope="scope">
          {{ scope.row.price }}
        </template>
      </el-table-column>
      <el-table-column label="种类">
        <template slot-scope="scope">
          {{ scope.row.category }}
        </template>
      </el-table-column>
      <el-table-column label="出版日期">
        <template slot-scope="scope">
          {{ scope.row.publication_date }}
        </template>
      </el-table-column>
      <el-table-column label="作者">
        <template slot-scope="scope">
          {{ scope.row.author }}
        </template>
      </el-table-column>
      <el-table-column label="索书号" width="110">
        <template slot-scope="scope">
          {{ scope.row.call_number }}
        </template>
      </el-table-column>
      <el-table-column label="总复本数量" width="110">
        <template slot-scope="scope">
          {{ scope.row.total_quantity }}
        </template>
      </el-table-column>
      <el-table-column label="可借复本数量" width="110">
        <template slot-scope="scope">
          {{ scope.row.borrowable_quantity }}
        </template>
      </el-table-column>
      <el-table-column label="借阅总次数" width="110">
        <template slot-scope="scope">
          {{ scope.row.borrowing_count }}
        </template>
      </el-table-column>
      <el-table-column label="馆藏分布" width="110">
        <template slot-scope="scope">
          <el-button type="text" @click="handleCollectionDistribution(scope.row.call_number)">馆藏情况</el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="260">
        <template slot-scope="scope">
          <div>
            <el-button size="small" type="primary" @click="updateBookInfoButton(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteBookInfoButton(scope.row)">删除</el-button>
            <el-button size="small" type="primary" @click="addBookButton(scope.row)">添加图书复本</el-button>
          </div>
        </template>
      </el-table-column>

    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="fetchData" />

    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      width="30%"
      center
    >
      <span>共{{ total }}条数据</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>

    <!-- Dialog 组件 -->
    <el-dialog :visible.sync="dialogVisibleImage" title="封面预览" width="30%">
      <img :src="imageUrl" style="width: 100%;" alt="预览">
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisibleImage = false">关 闭</el-button>
      </span>
    </el-dialog>

    <el-dialog :visible.sync="dialogVisibleBook" title="馆藏情况" width="70%">
      <el-table
        v-loading="searchLoading2"
        :data="listDistribution"
        element-loading-text="Loading"
        border
        fit
        highlight-current-row
      >
        <el-table-column align="center" label="ID" width="95">
          <template slot-scope="scope">
            {{ scope.$index }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="图书 ID" width="95">
          <template slot-scope="scope">
            {{ scope.row.book_id }}
          </template>
        </el-table-column>
        <el-table-column label="借阅状态">
          <template slot-scope="scope">
            {{ scope.row.status }}
          </template>
        </el-table-column>
        <el-table-column label="馆藏位置">
          <template slot-scope="scope">
            {{ scope.row.branch_location }}
          </template>
        </el-table-column>
        <el-table-column label="入库日期">
          <template slot-scope="scope">
            {{ scope.row.created_at }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <div>
              <el-button size="small" type="primary" @click="updateBookButton(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteBookButton(scope.row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisibleBook = false">关 闭</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="添加图书"
      :visible.sync="dialogVisibleAddBookInfo"
      width="70%"
      center
    >
      <el-form ref="listAdd" :model="listAdd" label-width="100px">
        <el-form-item label="书名" prop="title">
          <el-input v-model="listAdd.title" placeholder="请输入书名" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item label="出版社" prop="publisher">
          <el-input v-model="listAdd.publisher" placeholder="请输入出版社" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="listAdd.description" placeholder="请输入描述" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item label="ISBN" prop="isbn">
          <el-input v-model="listAdd.isbn" placeholder="请输入ISBN" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item label="封面图片" prop="cover_image">
          <el-upload
            :headers="headers"
            action="http://127.0.0.1:8000/api/upload-book-image/"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            accept="image/jpg,image/jpeg,image/png"
          >
            <el-button size="small" type="primary">点击上传</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="预览图片">
          <img v-if="listAdd.cover_image_path" :src="'http://127.0.0.1:8000/' + listAdd.cover_image_path" alt="预览图片" style="max-width: 200px; max-height: 200px;">
          <span v-else>暂无图片</span>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input v-model="listAdd.price" placeholder="请输入价格" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input v-model="listAdd.category" placeholder="请输入分类" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item label="出版日期" prop="publication_date">
          <el-input v-model="listAdd.publication_date" placeholder="请输入出版日期" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="listAdd.author" placeholder="请输入作者" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item label="索书号" prop="call_number">
          <el-input v-model="listAdd.call_number" placeholder="请输入索书号" clearable @clear="handleClearAddBookInfo()" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addBookInfo">添加</el-button>
          <el-button @click="dialogVisibleAddBookInfo = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog
      title="添加图书复本"
      :visible.sync="dialogVisibleAddBook"
      width="70%"
      center
    >
      <el-form ref="listAdd" :model="listAdd" label-width="100px">
        <el-form-item label="图书ID" prop="book_id">
          <el-input v-model="listAdd.book_id" placeholder="请输入图书ID" clearable @clear="handleClearAddBook()" />
        </el-form-item>
        <el-form-item label="分馆位置" prop="branch_location">
          <el-input v-model="listAdd.branch_location" placeholder="请输入分馆位置" clearable @clear="handleClearAddBook()" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-input v-model="listAdd.status" placeholder="请输入状态" clearable @clear="handleClearAddBook()" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addBook">添加</el-button>
          <el-button @click="dialogVisibleAddBook = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog
      title="编辑图书"
      :visible.sync="dialogVisibleUpdateBookInfo"
      width="70%"
      center
    >
      <el-form ref="listUpdate" :model="listUpdate" label-width="100px">
        <el-form-item label="书名" prop="title">
          <el-input v-model="listUpdate.title" placeholder="请输入书名" clearable @clear="handleClearUpdateBookInfo()" />
        </el-form-item>
        <el-form-item label="出版社" prop="publisher">
          <el-input v-model="listUpdate.publisher" placeholder="请输入出版社" clearable @clear="handleClearUpdateBookInfo()" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="listUpdate.description" placeholder="请输入描述" clearable @clear="handleClearUpdateBookInfo()" />
        </el-form-item>
        <el-form-item label="ISBN" prop="isbn">
          <el-input v-model="listUpdate.isbn" placeholder="请输入ISBN" clearable @clear="handleClearUpdateBookInfo()" />
        </el-form-item>
        <el-form-item label="封面图片" prop="cover_image">
          <el-upload
            :headers="headers"
            action="http://127.0.0.1:8000/api/upload-book-image"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            accept="image/jpg,image/jpeg,image/png"
          >
            <el-button size="small" type="primary">点击上传</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="预览图片">
          <img v-if="listUpdate.cover_image_path" :src="'http://127.0.0.1:8000/' + listAdd.cover_image_path" alt="预览图片" style="max-width: 200px; max-height: 200px;">
          <span v-else>暂无图片</span>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input v-model="listUpdate.price" placeholder="请输入价格" clearable @clear="handleClearUpdateBookInfo()" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input v-model="listUpdate.category" placeholder="请输入分类" clearable @clear="handleClearUpdateBookInfo()" />
        </el-form-item>
        <el-form-item label="出版日期" prop="publication_date">
          <el-input v-model="listUpdate.publication_date" placeholder="请输入出版日期" clearable @clear="handleClearUpdateBookInfo()" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="listUpdate.author" placeholder="请输入作者" clearable @clear="handleClearUpdateBookInfo()" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="updateBookInfo">修改</el-button>
          <el-button @click="dialogVisibleUpdateBookInfo = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog
      title="编辑图书复本"
      :visible.sync="dialogVisibleUpdateBook"
      width="70%"
      center
    >
      <el-form ref="listUpdate" :model="listUpdate" label-width="100px">
        <el-form-item label="分馆位置" prop="branch_location">
          <el-input v-model="listUpdate.branch_location" placeholder="请输入分馆位置" clearable @clear="handleClearUpdateBook()" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="updateBook">修改</el-button>
          <el-button @click="dialogVisibleUpdateBook = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog
      title="提示"
      :visible.sync="dialogVisibleDeleteBookInfo"
      width="30%"
      center
    >
      <span>确定要删除该图书信息？</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="danger" @click="deleteBookInfo">确 定</el-button>
        <el-button type="primary" @click="dialogVisibleDeleteBookInfo = false">取 消</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="提示"
      :visible.sync="dialogVisibleDeleteBook"
      width="30%"
      center
    >
      <span>确定要删除该图书复本？</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="danger" @click="deleteBook">确 定</el-button>
        <el-button type="primary" @click="dialogVisibleDeleteBook = false">取 消</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
import { bookSearch, getAllBooks, getBooksByCall, addBook, addBookInfo, deleteBookInfo, updateBookLocation, updateBookInfo, deleteBook } from '@/api/book'
import waves from '@/directive/waves' // waves directive
// import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'
import { getToken } from '@/utils/auth'
// import {rules} from "eslint-plugin-vue"; // secondary package based on el-pagination
// import {getList} from "@/api/table"; // 假设这是你的 API 导入语句

export default {
  name: 'BookSearch',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      list: [],
      total: 0,
      imageUrl: '',
      dialogVisibleUpdateBookInfo: false,
      dialogVisibleDeleteBookInfo: false,
      dialogVisibleUpdateBook: false,
      dialogVisibleDeleteBook: false,
      dialogVisible: false,
      dialogVisibleImage: false,
      dialogVisibleBook: false,
      searchLoading2: false,
      dialogVisibleAddBookInfo: false,
      dialogVisibleAddBook: false,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        call_number: undefined,
        title: undefined,
        publisher: undefined,
        sort: '+borrowing_count'
      },
      listAdd: {
        title: undefined,
        publisher: undefined,
        description: undefined,
        isbn: undefined,
        cover_image_path: undefined,
        price: undefined,
        category: undefined,
        publication_date: undefined,
        author: undefined,
        call_number: undefined,
        book_id: undefined,
        branch_location: undefined,
        status: undefined
      },
      listUpdate: {
        title: undefined,
        publisher: undefined,
        description: undefined,
        isbn: undefined,
        cover_image_path: undefined,
        price: undefined,
        category: undefined,
        publication_date: undefined,
        author: undefined,
        call_number: undefined,
        book_id: undefined,
        branch_location: undefined,
        status: undefined
      },
      listDistribution: [],
      searchText: '', // 用户输入的搜索关键字
      searchLoading: false, // 搜索加载状态
      deleteCallNumber: undefined,
      deleteBookID: undefined,
      distributionCallNumber: undefined
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
  // },
  created() {
    this.fetchData()
  },
  methods: {
    // 添加图书按钮
    addBookButton(row) {
      this.dialogVisibleAddBook = true
      this.listAdd.call_number = row.call_number
    },
    // 编辑图书按钮
    updateBookButton(row) {
      this.dialogVisibleUpdateBook = true
      this.listUpdate.book_id = row.book_id
    },
    // 编辑图书馆藏位置
    updateBook() {
      this.$refs['listUpdate'].validate((valid) => {
        if (valid) {
          const bookData = {
            book_id: this.listUpdate.book_id,
            branch_location: this.listUpdate.branch_location
          }
          updateBookLocation(bookData).then(response => {
            this.$message({
              message: '修改成功',
              type: 'success'
            })
            this.dialogVisibleUpdateBook = false
            this.fetchData()
          }).catch(error => {
            console.error('修改失败', error)
            this.dialogVisibleUpdateBook = false
          })
        }
      })
    },
    // 删除图书按钮
    deleteBookButton(row) {
      this.dialogVisibleDeleteBook = true
      this.deleteBookID = row.book_id
    },
    // 删除图书
    deleteBook() {
      const deleteBookData = {
        book_id: this.deleteBookID
      }
      deleteBook(deleteBookData).then(response => {
        this.$message({
          message: '删除成功',
          type: 'success'
        })
        this.dialogVisibleDeleteBook = false
        this.handleClearDeleteBook()
        getBooksByCall({ call_number: this.distributionCallNumber }).then(response => {
          this.listDistribution = response.data.items
          console.log(this.listDistribution)
          this.dialogVisibleBook = true
        }).catch(error => {
          console.error('获取图书馆藏分布失败', error)
        })
      }).catch(error => {
        console.error('删除失败', error)
        this.dialogVisibleDeleteBook = false
        this.handleClearDeleteBook()
      })
    },
    // 删除图书信息按钮
    deleteBookInfoButton(row) {
      this.dialogVisibleDeleteBookInfo = true
      this.deleteCallNumber = row.call_number
    },
    // 删除图书信息
    deleteBookInfo() {
      // console.log(this.deleteCallNumber)
      const deleteBookInfoData = {
        call_number: this.deleteCallNumber
      }
      deleteBookInfo(deleteBookInfoData).then(response => {
        this.$message({
          message: '删除成功',
          type: 'success'
        })
        this.dialogVisibleDeleteBookInfo = false
        this.handleClearDeleteBookInfo()
        this.fetchData()
      }).catch(error => {
        console.error('删除失败', error)
        this.dialogVisibleDeleteBookInfo = false
        this.handleClearDeleteBookInfo()
      })
    },
    // 修改图书信息按钮
    updateBookInfoButton(row) {
      this.dialogVisibleUpdateBookInfo = true
      this.listUpdate.call_number = row.call_number
    },
    // 修改图书信息
    updateBookInfo() {
      this.$refs['listUpdate'].validate((valid) => {
        if (valid) {
          const bookInfoData = {}
          for (const key in this.listUpdate) {
            if (this.listUpdate[key] !== undefined) {
              bookInfoData[key] = this.listUpdate[key]
            }
          }
          // console.log(bookInfoData)
          updateBookInfo(bookInfoData).then(response => {
            this.$message({
              message: '修改成功',
              type: 'success'
            })
            this.dialogVisibleUpdateBookInfo = false
            this.fetchData()
          }).catch(error => {
            console.error('修改失败', error)
            this.dialogVisibleUpdateBookInfo = false
          })
        }
      })
    },
    handleUploadSuccess(response) {
      if (response['code'] === 20000) {
        this.listAdd.cover_image_path = response.data.image_url
        console.log('上传成功', response.data.image_url)
        console.log(this.listAdd.cover_image_path)
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
    // 添加图书
    addBookInfo() {
      this.$refs['listAdd'].validate((valid) => {
        if (valid) {
          const bookInfoData = {
            title: this.listAdd.title,
            publisher: this.listAdd.publisher,
            description: this.listAdd.description,
            isbn: this.listAdd.isbn,
            cover_image_path: this.listAdd.cover_image_path,
            price: this.listAdd.price,
            category: this.listAdd.category,
            publication_date: this.listAdd.publication_date,
            author: this.listAdd.author,
            call_number: this.listAdd.call_number
          }
          addBookInfo(bookInfoData).then(response => {
            this.$message({
              message: '添加成功',
              type: 'success'
            })
            this.dialogVisibleAddBookInfo = false
            this.fetchData()
          }).catch(error => {
            console.error('添加失败', error)
            this.dialogVisibleAddBookInfo = false
          })
        }
      })
    },
    // 添加图书样书
    addBook() {
      this.$refs['listAdd'].validate((valid) => {
        if (valid) {
          const bookData = {
            call_number: this.listAdd.call_number,
            book_id: this.listAdd.book_id,
            branch_location: this.listAdd.branch_location,
            status: this.listAdd.status
          }
          addBook(bookData).then(response => {
            this.$message({
              message: '添加成功',
              type: 'success'
            })
            this.dialogVisibleAddBook = false
            this.fetchData()
          }).catch(error => {
            console.error('添加失败', error)
          })
        }
      })
    },
    // 查询该行 call_number 的图书的馆藏分布
    handleCollectionDistribution(call_number) {
      this.searchLoading2 = true
      const callNumberDistributionData = {
        call_number: call_number
      }
      this.distributionCallNumber = call_number
      getBooksByCall(callNumberDistributionData).then(response => {
        this.listDistribution = response.data.items
        console.log(this.listDistribution)
        this.dialogVisibleBook = true
      }).catch(error => {
        console.error('获取图书馆藏分布失败', error)
      })
      this.searchLoading2 = false
    },
    handleSearch() {
      if (this.listQuery.call_number === undefined) {
        this.listQuery.call_number = ''
      }
      if (this.listQuery.title === undefined) {
        this.listQuery.title = ''
      }
      if (this.listQuery.publisher === undefined) {
        this.listQuery.publisher = ''
      }
      this.searchLoading = true
      bookSearch(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.dialogVisible = true
        this.searchLoading = false
        this.$message({
          message: '图书搜索完成',
          type: 'success'
        })
      }).catch(error => {
        console.error('图书搜索失败', error)
        this.searchLoading = false
      })
    },
    handleClearSearch() {
      this.listQuery.call_number = undefined
      this.listQuery.title = undefined
      this.listQuery.publisher = undefined
    },
    handleClearAddBook() {
      this.listAdd.call_number = undefined
      this.listAdd.book_id = undefined
      this.listAdd.branch_location = undefined
      this.listAdd.status = undefined
    },
    handleClearUpdateBook() {
      this.listAdd.call_number = undefined
      this.listAdd.book_id = undefined
      this.listAdd.branch_location = undefined
      this.listAdd.status = undefined
    },
    handleClearAddBookInfo() {
      this.listAdd.title = undefined
      this.listAdd.publisher = undefined
      this.listAdd.description = undefined
      this.listAdd.isbn = undefined
      this.listAdd.cover_image_path = undefined
      this.listAdd.price = undefined
      this.listAdd.category = undefined
      this.listAdd.publication_date = undefined
      this.listAdd.author = undefined
      this.listAdd.call_number = undefined
    },
    handleClearUpdateBookInfo() {
      this.listAdd.title = undefined
      this.listAdd.publisher = undefined
      this.listAdd.description = undefined
      this.listAdd.isbn = undefined
      this.listAdd.cover_image_path = undefined
      this.listAdd.price = undefined
      this.listAdd.category = undefined
      this.listAdd.publication_date = undefined
      this.listAdd.author = undefined
      this.listAdd.call_number = undefined
    },
    handleClearDeleteBookInfo() {
      this.deleteCallNumber = undefined
    },
    handleClearDeleteBook() {
      this.deleteBookId = undefined
    },
    showFile(filePath) {
      // 设置要显示的图片路径
      this.imageUrl = 'http://127.0.0.1:8000/' + filePath
      // 打开 Dialog
      this.dialogVisibleImage = true
    },
    fetchData() {
      this.listLoading = true
      getAllBooks().then(response => {
        this.list = response.data.items
        console.log(this.list)
        this.total = response.data.total
        this.dialogVisible = true
        this.listLoading = false
      }).catch(error => {
        console.error('获取图书列表失败', error)
        this.listLoading = false
      })
    }
  }
}
</script>
