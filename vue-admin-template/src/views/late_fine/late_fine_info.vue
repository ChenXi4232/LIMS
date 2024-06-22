<template>
  <div class="app-container">
    <div class="filter-container">
      <!-- 搜索框和按钮 -->
      <el-input
        v-model="listQuery.book_id"
        placeholder="图书 ID"
        style="width: 200px;"
        class="filter-item"
        clearable
        @clear="handleClear()"
      />

      <el-input
        v-model="listQuery.reader_card_id"
        placeholder="读者证 ID"
        style="width: 200px;"
        class="filter-item"
        clearable
        @clear="handleClear()"
      />

      <el-input
        v-model="listQuery.status"
        placeholder="违期状态"
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
      <el-table-column label="违期 ID">
        <template slot-scope="scope">
          {{ scope.row.late_fee_id }}
        </template>
      </el-table-column>
      <el-table-column label="图书 ID">
        <template slot-scope="scope">
          {{ scope.row.book_id }}
        </template>
      </el-table-column>
      <el-table-column label="读者证 ID">
        <template slot-scope="scope">
          {{ scope.row.reader_card_id }}
        </template>
      </el-table-column>
      <el-table-column label="违期天数">
        <template slot-scope="scope">
          {{ scope.row.late_days }}
        </template>
      </el-table-column>
      <el-table-column label="罚款金额">
        <template slot-scope="scope">
          {{ scope.row.fine_amount }}
        </template>
      </el-table-column>
      <el-table-column label="处理状态">
        <template slot-scope="scope">
          {{ scope.row.status }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="125">
        <template slot-scope="scope">
          <div>
            <el-button size="small" type="primary" @click="updateStatusButton(scope.row)">更改违期状态</el-button>
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

    <el-dialog
      title="更改处理状态"
      :visible.sync="dialogVisibleStatus"
      width="70%"
      center
    >
      <el-form ref="status" :model="status" label-width="100px">
        <el-form-item label="违期处理状态" prop="status">
          <el-input v-model="status" placeholder="请输入更改后状态" clearable @clear="handleClearLateFeeID" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="updateStatus">更改</el-button>
          <el-button @click="dialogVisibleStatus = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>

<script>
import { findLateFeeInfo, getAllLateFeeInfo, updateLateFeeInfoStatus } from '@/api/late_fine_info'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination'
import user from '@/store'

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
      dialogVisibleStatus: false,
      dialogVisibleReserveBook: false,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        book_id: undefined,
        reader_card_id: undefined,
        status: undefined,
        // pickup_date: undefined,
        sort: '-fine_amount'
      },
      listDistribution: [],
      searchText: '', // 用户输入的搜索关键字
      searchLoading: false, // 搜索加载状态
      bookID: undefined,
      readerCardID: undefined,
      name: '',
      callNumber: undefined,
      late_fee_id: undefined,
      status: undefined
    }
  },
  // mounted() {
  //   this.fetchData()
  //   this.handleCollectionDistribution()
  // },
  created() {
    this.getUserInfo()
    this.fetchData()
  },
  methods: {
    // 更改处理状态按钮
    updateStatusButton(row) {
      this.dialogVisibleStatus = true
      this.late_fee_id = row.late_fee_id
    },
    // 更改处理状态
    updateStatus() {
      // console.log(this.name)
      const lateFeeData = {
        late_fee_id: this.late_fee_id,
        status: this.status
      }
      updateLateFeeInfoStatus(lateFeeData).then(response => {
        this.$message({
          message: '更改处理状态成功',
          type: 'success'
        })
        this.dialogVisibleStatus = false
        this.fetchData()
        this.handleClearStatus()
      }).catch(error => {
        console.error('更改处理状态失败', error)
        this.dialogVisibleStatus = false
        this.handleClearStatus()
      })
    },
    handleSearch() {
      if (this.listQuery.book_id === undefined) {
        this.listQuery.book_id = ''
      }
      if (this.listQuery.reader_card_id === undefined) {
        this.listQuery.reader_card_id = ''
      }
      if (this.listQuery.status === undefined) {
        this.listQuery.status = ''
      }
      // if (this.listQuery.pickup_date === undefined) {
      //   this.listQuery.pickup_date = ''
      // }
      this.searchLoading = true
      findLateFeeInfo(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.dialogVisible = true
        this.searchLoading = false
        this.$message({
          message: '违期记录搜索完成',
          type: 'success'
        })
      }).catch(error => {
        console.error('违期记录搜索失败', error)
        this.searchLoading = false
      })
    },
    handleClear() {
      this.listQuery.book_id = undefined
      this.listQuery.reader_card_id = undefined
      this.listQuery.status = undefined
      // this.listQuery.reservation_date = undefined
    },
    handleClearLateFeeID() {
      this.late_fee_id = undefined
    },
    handleClearStatus() {
      this.status = undefined
    },
    // handleClearReaderCardID() {
    //   this.readerCardID = undefined
    // },
    // showFile(filePath) {
    //   // 设置要显示的图片路径
    //   // 利用 readAsDataURL 方法将文件读取为 DataURL
    //   this.imageUrl = 'http://127.0.0.1:8000/' + filePath
    //   // 读取文件
    //   // 打开 Dialog
    //   this.dialogVisibleImage = true
    // },
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
      getAllLateFeeInfo(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.dialogVisible = true
        this.listLoading = false
        this.$message({
          message: '违期记录查询完成',
          type: 'success'
        })
      }).catch(error => {
        console.error('违期记录查询失败', error)
        this.listLoading = false
      })
    }
  }
}
</script>
