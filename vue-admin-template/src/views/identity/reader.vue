<template>
  <div class="app-container">

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
      <el-table-column label="Title">
        <template slot-scope="scope">
          {{ scope.row.fields.title }}
        </template>
      </el-table-column>
      <el-table-column label="Publisher">
        <template slot-scope="scope">
          {{ scope.row.fields.publisher }}
        </template>
      </el-table-column>
      <el-table-column label="Description">
        <template slot-scope="scope">
          {{ scope.row.fields.description }}
        </template>
      </el-table-column>
      <el-table-column label="ISBN">
        <template slot-scope="scope">
          {{ scope.row.fields.isbn }}
        </template>
      </el-table-column>
      <el-table-column label="Cover Image">
        <template slot-scope="scope">
          <el-button type="text" @click="showFile(scope.row.fields.cover_image_path)">封面预览</el-button>
        </template>
      </el-table-column>
      <el-table-column label="Price">
        <template slot-scope="scope">
          {{ scope.row.fields.price }}
        </template>
      </el-table-column>
      <el-table-column label="Category">
        <template slot-scope="scope">
          {{ scope.row.fields.category }}
        </template>
      </el-table-column>
      <el-table-column label="Publication Date">
        <template slot-scope="scope">
          {{ scope.row.fields.publication_date }}
        </template>
      </el-table-column>
      <el-table-column label="Author">
        <template slot-scope="scope">
          {{ scope.row.fields.author }}
        </template>
      </el-table-column>
      <el-table-column label="Call Number" width="110">
        <template slot-scope="scope">
          {{ scope.row.fields.call_number }}
        </template>
      </el-table-column>
      <el-table-column label="Total Quantity" width="110">
        <template slot-scope="scope">
          {{ scope.row.fields.total_quantity }}
        </template>
      </el-table-column>
      <el-table-column label="Borrowable Quantity" width="110">
        <template slot-scope="scope">
          {{ scope.row.fields.borrowable_quantity }}
        </template>
      </el-table-column>
      <el-table-column label="Borrowing Count" width="110">
        <template slot-scope="scope">
          {{ scope.row.fields.borrowing_count }}
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
        <el-button @click="dialogVisibleImage = false">Close</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { bookSearch, getAllBooks } from '@/api/book_search'
import waves from '@/directive/waves' // waves directive
// import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
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
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        call_number: undefined,
        title: undefined,
        publisher: undefined,
        sort: '+borrowing_count'
      },
      searchText: '', // 用户输入的搜索关键字
      searchLoading: false // 搜索加载状态
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    handleSearch() {
      this.searchLoading = true
      bookSearch(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.dialogVisible = true
        this.searchLoading = false
      }).catch(error => {
        console.error('图书搜索失败', error)
        this.searchLoading = false
      })
    },
    handleClear() {
      this.searchText = ''
    },
    showFile(filePath) {
      // 设置要显示的图片路径
      this.imageUrl = filePath
      // 打开 Dialog
      this.dialogVisibleImage = true
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
