<template>
    <el-container>
        <el-header>
            <el-button type="primary" round @click="save">保存</el-button>
            <el-button type="danger" round @click="del">删除</el-button>
            <el-button type="danger" round @click="back">返回</el-button>
        </el-header>
        <el-main>
            <el-form :inline="true" :model="formData" label-position="top">
                <el-form-item label="过滤器名称">
                    <el-input v-model="formData.new_name" placeholder="" clearable />
                </el-form-item>
                <el-form-item label="说明">
                    <el-input type="textarea" autosize v-model="formData.new_memo" placeholder="" clearable />
                </el-form-item>
                <el-form-item label="函数">
                    <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 10}" v-model="formData.new_func" placeholder="" clearable />
                </el-form-item>
                <el-form-item label="创建时间">
                    <el-date-picker v-model="formData.new_createdon" type="datetime" placeholder="Empty" disabled />
                </el-form-item>
                <el-form-item label="修改时间">
                    <el-date-picker v-model="formData.new_modifiedon" type="datetime" placeholder="Empty" disabled />
                </el-form-item>
            </el-form>
        </el-main>
    </el-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import req from '../common/interface'
import { useRouter } from "vue-router";
import { ElMessage, ElNotification, ElMessageBox } from 'element-plus';
import { Plus,RefreshRight } from '@element-plus/icons-vue';
const router = useRouter()
var id = ref("")

var formData = ref({
    new_filterid: id.value,
    new_name: "",
    new_note: "",
    new_createdon: "",
    new_modifiedon: "",
});
var tableData = ref([]);

onMounted(() => {
    id.value = router.currentRoute.value.query.id;
    loadData();
})

/**加载数据 */
function loadData() {
    if (id.value) {
        req.get(`/api/new_filter/get/?id=${id.value}`).then(res => {
            console.log("res", res.data);
            formData.value = res.data;
        }).catch(err => {
            console.error(err);
        });
    }
}

/**保存 */
function save() {
    req.post("/api/new_filter/save/", formData.value).then(res => {
        console.log("res", res);
        id.value = res.data;
        ElMessage.success("保存成功!")
        loadData();
    }).catch(err => {
        console.error(err);
    });
}


function create() {
    // id.value = ""
    // formData.value = {
    //     new_template_groupid: id.value,
    //     new_name: "",
    //     new_note: "",
    //     new_createdon: "",
    //     new_modifiedon: "",
    // }
    // 路由跳转有问题
    router.push("/TemplateGroupEdit");
}

/**删除 */
function del() {
    req.post("/api/new_filter/delete/", [id.value]).then(res => {
        console.log("res", res);
        back();
    }).catch(err => {
        console.error(err);
    });
}

/**路由回退 */
function back() {
    router.back();
}

</script>

<style scoped></style>