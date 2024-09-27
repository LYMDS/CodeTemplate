<template>
  <el-container>
    <el-header>
      <el-button type="primary" round @click="save">保存</el-button>
      <el-button type="success" round @click="create">新建</el-button>
      <el-button type="danger" round @click="del">删除</el-button>
      <el-button type="success" round @click="render">生成</el-button>
      <el-button type="primary" round @click="download">下载模板</el-button>
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
          <el-date-picker
            v-model="formData.new_createdon"
            type="datetime"
            placeholder="Empty"
            disabled
          />
        </el-form-item>
        <el-form-item label="修改时间">
          <el-date-picker
            v-model="formData.new_modifiedon"
            type="datetime"
            placeholder="Empty"
            disabled
          />
        </el-form-item>
      </el-form>
      <el-table v-show="id"
        ref="tableRef"
        :data="tableData"
        style="width: 100%"
        @row-dblclick="dblclick"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="new_name" label="参数名" width="180" />
        <el-table-column prop="new_type" label="参数类型" width="180" />
        <el-table-column prop="new_value" label="参数值" width="180" />
        <el-table-column prop="new_createdon" label="创建时间" width="180" />
        <el-table-column prop="new_modifiedon" label="修改时间" width="180" />
        <el-table-column align="right">
          <template #header>
            <el-button
              size="small"
              :icon="Plus"
              type="success"
              circle
              @click="createLine"
            ></el-button>
            <el-button
              size="small"
              :icon="RefreshRight"
              type="success"
              circle
              @click="refreshLine"
            ></el-button>
          </template>
          <template #default="scope">
            <el-button
              size="small"
              @click="handleEdit(scope.$index, scope.row)"
            >
              Edit
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
            >
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-upload
        :v-model:file-list="fileList"
        :action="req.BaseUrl + '/api/new_attachment/upload/'"
        :limit="1"
        :on-success="fileUploadSuccess"
      >
        <el-button type="primary">上传模板</el-button>
      </el-upload>
    </el-main>
    <el-dialog v-model="dialogCodeVisible" title="代码" width="88%">
    <el-input type="textarea" 
    v-model="codeString" :rows="18" style="width: 100%"
    ></el-input>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogCodeVisible = false">关闭</el-button>
        <el-button type="primary" @click="dialogCodeVisible = false">复制</el-button>
      </div>
    </template>
  </el-dialog>
  </el-container>
</template>

<script setup>
import { onMounted, ref } from "vue";
import req from "../common/interface";
import { useRouter } from "vue-router";
import { RefreshRight, Plus } from "@element-plus/icons-vue";
import { ElMessage, ElNotification, ElMessageBox } from "element-plus";

const router = useRouter();
var id = ref("");
var new_template_group_id = ref("");

var formData = ref({
  new_template_contentid: id.value,
  new_template_group_id: new_template_group_id.value,
  new_content: "",
  new_file_name: "",
  new_file_type: "",
  new_createdon: "",
  new_modifiedon: "",
  new_attachment_id: "",
});
var tableData = ref([]);
var fileList = ref([]);
var dialogCodeVisible = ref(false)
var codeString = ref("")
onMounted(() => {
  id.value = router.currentRoute.value.query.id;
  new_template_group_id.value =
    router.currentRoute.value.query.new_template_group_id;
  if (!new_template_group_id.value) {
    ElMessage.error("缺失主档模板组!");
  } else {
    formData.value.new_template_group_id = new_template_group_id.value;
  }
  loadData();
  loadLine();
});

/**加载数据 */
function loadData() {
  if (id.value) {
    req
      .get(`/api/new_template_content/get/?id=${id.value}`)
      .then((res) => {
        console.log("res", res.data);
        formData.value = res.data;
      })
      .catch((err) => {
        console.error(err);
      });
  }
}

/**加载明细 */
function loadLine() {
  if (id.value) {
    req.get(`/api/new_template_param/getlistbycontentid/?id=${id.value}`).then(res => {
        console.log("res", res.data);
        tableData.value = res.data;
    }).catch(err => {
      ElMessage.error(err)
    });
  }
}

/**保存 */
function save() {
  req
    .post("/api/new_template_content/save/", formData.value)
    .then((res) => {
      console.log("res", res);
      id.value = res.data;
      loadData();
    })
    .catch((err) => {
      console.error(err);
    });
}

function create() {
  id.value = ""
  formData.value = {
    new_template_contentid: id.value,
    new_template_group_id: new_template_group_id.value,
    new_content: "",
    new_file_name: "",
    new_file_type: "",
    new_createdon: "",
    new_modifiedon: "",
    new_attachment_id: "",
  }
  tableData.value = [];
  fileList.value = [];
}

/**删除 */
function del() {
  req.post("/api/new_template_content/delete/", [id.value]).then(res => {
      console.log("res", res);
      back();
  }).catch(err => {
      console.error(err);
  });
}

/**刷新明细 */
function refreshLine() {
  loadLine();
}

/**文件上传成功 */
function fileUploadSuccess(fileId) {
  formData.value.new_attachment_id = fileId;
  save();
}

/**文件下载 */
function download() {
  if (formData.value.new_attachment_id) {
    req.opendownload(
      `/api/new_attachment/download/?id=${formData.value.new_attachment_id}`
    );
  } else {
    ElMessage.error("未上传附件,不可下载!");
  }
}
/**路由回退 */
function back() {
  router.back();
}

/**跳转内容明细 */
function dblclick(event) {
    router.push({
        path: "/TemplateParamEdit",
        query: {
            id: event.new_template_paramid,
            new_template_group_id: new_template_group_id.value,
            new_template_code_id: id.value
        }
    });
}

/**跳转内容明细 */
function handleEdit(index, event) {
  dblclick(event);
}

/**创建明细 */
function createLine() {
  router.push({
      path: "/TemplateParamEdit",
      query: {
          id: "",
          new_template_group_id: new_template_group_id.value,
          new_template_code_id: id.value
      }
  });
}

/**生成当前文档并预览 */
function render() {
  req.get(`/api/templaterender/template_content/?id=${id.value}`).then(res => {
        // console.log("/api/templaterender/template_content/=>res", res.data);
        codeString.value = res.data;
        dialogCodeVisible.value = true;
    }).catch(err => {
      ElMessage.error(err)
    });
}

</script>

<style scoped></style>
