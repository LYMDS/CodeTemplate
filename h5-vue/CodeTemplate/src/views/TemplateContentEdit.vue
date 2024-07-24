<template>
    <el-container>
        <el-header>
            <el-button type="primary" round @click="save">保存</el-button>
            <el-button type="success" round @click="create">新建</el-button>
            <el-button type="danger" round @click="del">删除</el-button>
            <el-button type="danger" round @click="back">返回</el-button>
        </el-header>
        <el-main>
            <el-form :inline="true" :model="formData" label-position="top">
                <el-form-item label="文件名">
                    <el-input v-model="formData.new_file_name" placeholder="" clearable />
                </el-form-item>
                <el-form-item label="文件类型">
                    <el-input v-model="formData.new_file_type" placeholder="" clearable />
                </el-form-item>
                <el-form-item label="文件内容">
                    <el-input v-model="formData.new_content" placeholder="" clearable />
                </el-form-item>
                <el-form-item label="创建时间">
                    <el-date-picker v-model="formData.new_createdon" type="datetime" placeholder="Empty" disabled />
                </el-form-item>
                <el-form-item label="修改时间">
                    <el-date-picker v-model="formData.new_modifiedon" type="datetime" placeholder="Empty" disabled />
                </el-form-item>
            </el-form>
            <!-- <el-table ref="tableRef" :data="tableData" style="width: 100%">

                <el-table-column type="selection" width="55" />
                <el-table-column prop="new_file_name" label="######" width="180" />
                <el-table-column prop="new_content" label="######" width="180" />
                <el-table-column prop="new_file_type" label="######" width="180" />
                <el-table-column prop="new_createdon" label="######" width="180" />
                <el-table-column prop="new_modifiedon" label="######" width="180" />
                <el-table-column align="right">
                    <template #header>
                        <el-button size="small" :icon="RefreshRight" type="success" circle @click="refreshLine"></el-button>
                    </template>
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
                            编辑
                        </el-button>
                        <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table> -->
        </el-main>
    </el-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import req from '../common/interface'
import { useRouter } from "vue-router";
import { RefreshRight } from '@element-plus/icons-vue'
import { ElMessage,ElNotification,ElMessageBox } from 'element-plus';
const router = useRouter()
var id = ref("")
var new_template_group_id = ref("")

var formData = ref({
    new_template_contentid: id.value,
    new_template_group_id: new_template_group_id.value,
    new_content: "",
    new_file_name: "",
    new_file_type: "",
    new_createdon: "",
    new_modifiedon: "",
});
var tableData = ref([]);

onMounted(() => {
    id.value = router.currentRoute.value.query.id;
    new_template_group_id.value = router.currentRoute.value.query.new_template_group_id;
    if (!new_template_group_id.value) {
        ElMessage.error("缺失主档模板组!")
    } else {
        formData.value.new_template_group_id = new_template_group_id.value;
    }
    debugger;
    loadData();
    loadLine();
})

/**加载数据 */
function loadData() {
    if (id.value) {
        req.get(`/api/new_template_content/get/?id=${id.value}`).then(res => {
            console.log("res", res.data);
            formData.value = res.data;
        }).catch(err => {
            console.error(err);
        });
    }
}

/**加载明细 */
function loadLine() {
    if (id.value) {
        // req.get(`/api/new_template_content/getlistbygroupid/?id=${id.value}`).then(res => {
        //     console.log("res", res.data);
        //     tableData.value = res.data;
        // }).catch(err => {
        //     console.error(err);
        // });
    }
}

/**保存 */
function save() {
    req.post("/api/new_template_content/save/", formData.value).then(res => {
        console.log("res", res);
        id.value = res.data;
        loadData();
    }).catch(err => {
        console.error(err);
    });
}

function create() {
    // id.value = ""
    // formData.value = {
    //     new_template_group_id: id.value,
    //     new_name: "",
    //     new_note: "",
    //     new_createdon: "",
    //     new_modifiedon: "",
    // }
}

/**删除 */
function del() {
    // req.post("/api/new_template_group/delete/", [id.value]).then(res => {
    //     console.log("res", res);
    //     back();
    // }).catch(err => {
    //     console.error(err);
    // });
}

/**刷新明细 */
function refreshLine() {
    loadLine();
}

/**路由回退 */
function back() {
    router.back();
}

</script>

<style scoped></style>