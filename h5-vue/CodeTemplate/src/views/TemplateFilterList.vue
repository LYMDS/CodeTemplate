<template>
    <el-container>
        <el-header>
            <el-button type="primary" round @click="refresh">刷新</el-button>
            <el-button type="success" round @click="create">新建</el-button>
            <el-button type="danger" round @click="del">删除</el-button>
            <el-input class="searchstr_input" v-model="searchStr" placeholder="搜索" />
        </el-header>
        <el-main>
            <el-table ref="tableRef" :data="tableData" style="width: 100%" @row-dblclick="dblclick">
                <el-table-column type="selection" width="55" />
                <el-table-column prop="new_name" label="过滤器名称" width="180" />
                <el-table-column prop="new_memo" label="说明" width="180" />
                <el-table-column prop="new_func" label="函数" width="180" />
                <el-table-column prop="new_createdon" label="创建时间" width="180" />
                <el-table-column prop="new_modifiedon" label="修改时间" width="180" />
            </el-table>
        </el-main>
    </el-container>
    
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from "vue-router";
import req from '../common/interface'
import { ElMessage, ElNotification, ElMessageBox } from 'element-plus';
const router = useRouter()
var tableRef = ref();
var tableData = ref([]);
var searchStr = ref("");
var dialogFormVisible = ref(false);
var form = ref({new_name:"",new_memo:"",new_func:""});

onMounted(() => {
    getData();
})

/**获取数据 */
function getData() {
    req.get(`/api/new_filter/getlist/?search=${searchStr.value}`).then(res => {
        tableData.value = res.data;
    }).catch(err => {
        console.error(err);
    })
}

/**双击跳转 */
function dblclick(event) {
    router.push({
        path: "/TemplateFilterEdit",
        query: {
            id: event.new_filterid
        }
    });
}

function create() {
    router.push("/TemplateFilterEdit");
}

/**刷新按钮 */
function refresh() {
    getData();
}

/**删除按钮 */
function del() {
    var selectedList = tableRef.value.getSelectionRows();
    if (selectedList && selectedList.length > 0) {
        ElMessageBox.confirm("确定永久删除这条记录吗?", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
        }).then(() => {
            var deleteIds = selectedList.map(s => s.new_filterid);
            req.post("/api/new_filter/delete/", deleteIds).then(res => {
                getData();
                ElMessage.success("删除成功!")
            }).catch(err => {
                ElMessage.error(err)
            });
        }).catch(() => {
            ElMessage.success("已取消!")
        })
    } else {
        ElMessage.error("请至少选择一行!")
    }
}

</script>

<style scoped>
.searchstr_input {
    width: 240px;
    position: absolute;
    right: 15px;
}
</style>