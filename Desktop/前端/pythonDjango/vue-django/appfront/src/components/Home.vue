<template>
  <div class="home">
    <router-link to="/login">登录</router-link>
    <router-link to="/HelloWorld">HelloWorld</router-link>
    <el-row display="margin-top:10px">
        <el-input v-model="input" placeholder="请输入书名" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-button type="primary" size="medium" @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
    </el-row>
    <el-row>
        <el-table :data="bookList" style="width: 100%" border>
          <el-table-column prop="id" label="编号" min-width="100">
            <template scope="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="book_name" label="书名" min-width="100">
            <template scope="scope"> {{ scope.row.fields.book_name }} </template>
          </el-table-column>
          <el-table-column prop="add_time" label="添加时间" min-width="100">
            <template scope="scope"> {{ scope.row.fields.add_time }} </template>
          </el-table-column>
           <el-table-column
        label="操作"
        width="150px"
      >
        <template slot-scope="scope">
          <el-button
            type="text"
            @click="edit(scope.row)"
          >修改</el-button>
          <el-button
            type="text"
            @click="deletebook(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
      </el-table>
    </el-row>
    <!----修改表单--->
    <el-dialog title="修改书籍" :visible.sync="dialogFormVisible">
    <el-form :model="form">
      <el-form-item label="书籍名称" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off"></el-input>
      </el-form-item>
    </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="confirm()">确 定</el-button>
  </div>
</el-dialog>

  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      input: '',
      bookList: [],
      editParams: '',
      dialogFormVisible: false,
        form: {
          name: ''
        },
    }
  },
  mounted: function () {
    this.showBooks()
  },
  methods: {
  //添加
    addBook () {
      if(this.input === '' || this.input === null){
        this.$message.error('请输入书籍名称。')
        return
      }
      this.$http.get('http://127.0.0.1:8000/api/add_book?book_name=' + this.input)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          if (res.error_num === 0) {
            this.showBooks()
            this.$message.success('新增书籍成功。')
          } else {
            this.$message.error('新增书籍失败，请重试')
            console.log(res['msg'])
          }
        })
    },
    //查询
    showBooks () {
      this.$http.get('http://127.0.0.1:8000/api/show_books')
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.bookList = res['list']
          } else {
            this.$message.error('查询书籍失败')
            console.log(res['msg'])
          }
        })
    },
    //修改
    edit(rows){
     this.dialogFormVisible = true
     this.form.name =''
     this.editParams = rows

    },
    confirm(){
      const date = '2020-08-20T11:54:44.544Z'
      this.$http.get('http://127.0.0.1:8000/api/update_book?book_name=' + this.form.name+'&book_id='+ this.editParams.pk+'&add_time='+ date)
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num === 0) {
              this.showBooks()
              this.$message.success('修改成功。')
              this.dialogFormVisible = false
            } else {
              this.$message.error('修改书籍失败，请重试')
              console.log(res['msg'])
              this.dialogFormVisible = false
            }
          })
    },
    //删除
    deletebook(rows){
      this.$http.get('http://127.0.0.1:8000/api/delete_book?book_id=' + rows.pk)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          if (res.error_num === 0) {
            this.showBooks()
            this.$message.success('删除成功。')
          } else {
            this.$message.error('删除书籍失败，请重试')
            console.log(res['msg'])
          }
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
