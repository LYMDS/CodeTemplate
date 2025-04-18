<template>
    <el-container  v-loading="loading">
        <el-header>
            <el-button type="primary" round @click="refresh">刷新</el-button>
            <el-button type="success" round @click="create">新建</el-button>
            <el-button type="danger" round @click="del">删除</el-button>
            <el-input class="searchstr_input" v-model="searchStr" placeholder="搜索" :spellcheck="false"/>
        </el-header>
        <el-main>
            <el-table ref="tableRef" :data="tableData" style="width: 100%" @row-dblclick="dblclick">
                <el-table-column type="selection" width="55" />
                <el-table-column prop="name" label="驱动器名称" width="180" />
                <el-table-column prop="desc" label="说明" width="180" :show-overflow-tooltip="true" />
                <el-table-column prop="type" label="类型" width="180">
                    <template #default="scope">
                        {{getTypeLabelName(scope.row.type)}}
                        
                    </template>
                </el-table-column>
                <el-table-column prop="createdon" label="创建时间" width="180" />
                <el-table-column prop="modifiedon" label="修改时间" width="180" />
            </el-table>
        </el-main>
    </el-container>
    
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from "vue-router";
import req from '../common/interface'
import { ElMessage, ElNotification, ElMessageBox } from 'element-plus';
var loading = ref(false);
const router = useRouter()
var tableRef = ref();
var tableData = ref([]);
var searchStr = ref("");
var typeOptionSet = ref([]);
getTypeOptionSet();
onMounted(() => {
    getData();
})

/**获取数据 */
function getData() {
    loading.value = true;
    req.get(`/api/datadriver/getlist/?search=${searchStr.value}`).then(res => {
        tableData.value = res.data;
        loading.value = false;
    }).catch(err => {
        loading.value = false;
        console.error(err);
    })
}

/**获取驱动类型列表 */
function getTypeOptionSet() {
    req.get("/api/datadriver/gettypeoptionset/").then(res => {
        typeOptionSet.value = res.data;
    }).catch(err => {
        ElMessage.error(err);
    })
}

/**获取驱动类型标签 */
function getTypeLabelName(value) {
    const os = typeOptionSet.value.find(t => t.value == value);
    if (os) return os.name;
    else return "";
}

/**双击跳转 */
function dblclick(event) {
    router.push({
        path: "/DataDriverEdit",
        query: {
            id: event.datadriverid
        }
    });
}

function create() {
    router.push("/DataDriverCreate");
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
            loading.value = true;
            var deleteIds = selectedList.map(s => s.datadriverid);
            req.post("/api/datadriver/delete/", deleteIds).then(res => {
                loading.value = false;
                getData();
                ElMessage.success("删除成功!")
            }).catch(err => {
                loading.value = false;
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