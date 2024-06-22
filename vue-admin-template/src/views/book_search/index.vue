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
        @clear="handleClear()"
      />

      <el-input
        v-model="listQuery.publisher"
        placeholder="出版社"
        style="width: 100px;"
        class="filter-item"
        clearable
        @clear="handleClear()"
      />

      <el-input
        v-model="listQuery.call_number"
        placeholder="索书号"
        style="width: 200px;"
        class="filter-item"
        clearable
        @clear="handleClear()"
      />

      <el-button
        type="primary"
        :loading="searchLoading"
        @click="handleSearch()"
      >
        搜索
      </el-button>
    </div>

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
        v-loading="searchLoading"
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
              <el-button size="small" type="primary" @click="reserveBook(scope.row)">预约</el-button>
              <el-button size="small" type="danger" @click="borrowBook(scope.row)">借阅</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisibleBook = false">关 闭</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="借书"
      :visible.sync="dialogVisibleBorrowBook"
      width="70%"
      center
    >
      <el-form ref="readerCardID" :model="readerCardID" label-width="100px">
        <el-form-item label="读者证 ID" prop="reader_card_id">
          <el-input v-model="readerCardID" placeholder="请输入读者证 ID" clearable @clear="handleClearReaderCardID" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="borrowBook">借书</el-button>
          <el-button @click="dialogVisibleBorrowBook = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog
      title="预约"
      :visible.sync="dialogVisibleReserveBook"
      width="70%"
      center
    >
      <el-form ref="readerCardID" :model="readerCardID" label-width="100px">
        <el-form-item label="读者证 ID" prop="reader_card_id">
          <el-input v-model="readerCardID" placeholder="请输入读者证 ID" clearable @clear="handleClearReaderCardID" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="reserveBook">预约</el-button>
          <el-button @click="dialogVisibleReserveBook = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>

<script>
import { bookSearch, getAllBooks, getBooksByCall, borrowBook, reserveBook } from '@/api/book_search'
import waves from '@/directive/waves' // waves directive
// import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'
import user from '@/store'
// import { deleteBook } from "@/api/book"; // secondary package based on el-pagination
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
      dialogVisible: false,
      dialogVisibleImage: false,
      dialogVisibleBook: false,
      dialogVisibleBorrowBook: false,
      dialogVisibleReserveBook: false,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        call_number: undefined,
        title: undefined,
        publisher: undefined,
        sort: '+borrowing_count'
      },
      listDistribution: [],
      searchText: '', // 用户输入的搜索关键字
      searchLoading: false, // 搜索加载状态
      bookID: undefined,
      readerCardID: undefined,
      name: '',
      callNumber: undefined
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
    // 预约按钮
    reserveBookButton(row) {
      this.dialogVisibleReserveBook = true
      this.bookID = row.book_id
    },
    // 预约图书
    reserveBook(row) {
      // console.log(this.name)
      const reserveBookData = {
        reader_card_id: this.name,
        book_id: row.book_id
      }
      // console.log(reserveBookData)
      reserveBook(reserveBookData).then(response => {
        this.$message({
          message: '预约成功',
          type: 'success'
        })
        this.handleCollectionDistribution(this.callNumber)
      }).catch(error => {
        console.error('预约失败', error)
      })
      this.dialogVisibleReserveBook = false
      this.handleClearBookID()
    },
    // 借阅按钮
    borrowBookButton(row) {
      this.dialogVisibleBorrowBook = true
      this.bookID = row.book_id
    },
    // 借阅图书
    borrowBook(row) {
      const borrowBookData = {
        reader_card_id: this.name,
        book_id: row.book_id
      }
      borrowBook(borrowBookData).then(response => {
        this.$message({
          message: '借书成功',
          type: 'success'
        })
        this.handleCollectionDistribution(this.callNumber)
      }).catch(error => {
        console.error('借书失败', error)
      })
      this.dialogVisibleBorrowBook = false
      this.handleClearBookID()
    },
    // 查询该行 call_number 的图书的馆藏分布
    handleCollectionDistribution(call_number) {
      // this.searchLoading = true
      this.callNumber = call_number
      const callNumberDistributionData = {
        call_number: call_number
      }
      getBooksByCall(callNumberDistributionData).then(response => {
        this.listDistribution = response.data.items
        this.dialogVisibleBook = true
        // this.searchLoading = false
      }).catch(error => {
        console.error('获取图书馆藏分布失败', error)
        // this.searchLoading = false
      })
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
    handleClear() {
      this.listQuery.call_number = undefined
      this.listQuery.title = undefined
      this.listQuery.publisher = undefined
    },
    handleClearBookID() {
      this.bookID = undefined
    },
    handleClearReaderCardID() {
      this.readerCardID = undefined
    },
    showFile(filePath) {
      // 设置要显示的图片路径
      // 利用 readAsDataURL 方法将文件读取为 DataURL
      this.imageUrl = 'http://127.0.0.1:8000/' + filePath
      // 读取文件
      // 打开 Dialog
      this.dialogVisibleImage = true
    },
    getUserInfo() {
      // getInfo().then(response => {
      //   this.name = response.data.name
      // }).catch(error => {
      //   console.error('获取用户信息失败', error)
      // })
      this.name = user.getters.name
    },
    fetchData() {
      this.listLoading = true
      getAllBooks().then(response => {
        this.list = response.data.items
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
