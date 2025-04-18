<template>
  <el-container v-loading="loading">
    <el-header>
      <el-button type="primary" round @click="save">保存</el-button>
      <el-button type="success" round @click="create">新建</el-button>
      <el-button type="danger" round @click="del">删除</el-button>
      <el-button type="success" round @click="render">生成</el-button>
      <el-button type="danger" round @click="preview">预览模板</el-button>
      <el-upload 
        :v-model:file-list="fileList"
        :action="req.BaseUrl + '/api/new_attachment/upload/'"
        :limit="1"
        :on-success="fileUploadSuccess"
        style="margin-left: 12px;display: inline-flex;"
      >
        <el-button type="primary" round>上传模板</el-button>
      </el-upload>
      <el-button type="primary" round @click="download" style="margin-left: 12px;">下载模板</el-button>
      <el-button type="danger" round @click="back">返回</el-button>
    </el-header>
    <el-main>
      <el-form :inline="true" :model="formData" label-position="top">
        <el-form-item label="文件名">
          <el-input v-model="formData.new_file_name" placeholder="" clearable :spellcheck="false"/>
        </el-form-item>
        <el-form-item label="文件类型">
          <el-input v-model="formData.new_file_type" placeholder="" clearable :spellcheck="false"/>
        </el-form-item>
        <el-form-item label="文件内容">
          <el-input v-model="formData.new_content" placeholder="" clearable :spellcheck="false"/>
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
      <el-collapse v-model="activeCollapseNames">
        <el-collapse-item title="参数列表" name="1">
          <ParamEditor :type="2" :id="id" :groupid="new_template_group_id" />
        </el-collapse-item>
      </el-collapse>
    </el-main>
    <el-dialog v-loading="loadingDialog" v-model="dialogCodeVisible" :show-close="false" width="70%">
      <template #header="{ close, titleId, titleClass }">
        <div class="my-header">
          <h4 :id="titleId" :class="titleClass">模板内容</h4>
          <template v-if="!isrender && previeworedit">
            <el-button
              @click="editcode"
              circle
              :icon="Edit"
              size="small"
            ></el-button>
          </template>
          <template v-if="!isrender && !previeworedit">
            <el-button
              @click="savecode"
              circle
              :icon="Finished"
              size="small"
            ></el-button>
            <el-button
              type="primary"
              @click="preview"
              circle
              :icon="Back"
              size="small"
            ></el-button>
          </template>
          <el-button
            type="danger"
            @click="close"
            circle
            :icon="Close"
            size="small"
          ></el-button>
        </div>
      </template>

      <!-- 预览当前模板 -->
      <div v-if="!isrender && previeworedit" v-html="codeString"></div>
      <!-- 编辑当前模版 -->
      <el-input
        v-if="!previeworedit || isrender"
        :spellcheck="false"
        :autosize="true"
        type="textarea"
        v-model="codeString"
        style="width: 100%"
      ></el-input>
      <template #footer>
        <div class="dialog-footer"></div>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { onMounted, ref } from "vue";
import req from "../common/interface";
import { useRouter } from "vue-router";
import {
  RefreshRight,
  Plus,
  Delete,
  Edit,
  Back,
  Close,
  Finished,
} from "@element-plus/icons-vue";
import { ElMessage, ElNotification, ElMessageBox } from "element-plus";
import ParamEditor from "../components/ParamEditor.vue";
var loading = ref(false);
var loadingDialog = ref(false);
const router = useRouter();
var id = ref("");
id.value = router.currentRoute.value.query.id;
var new_template_group_id = ref("");
new_template_group_id.value =
  router.currentRoute.value.query.new_template_group_id;
var formData = ref({
  new_template_contentid: id.value || "",
  new_template_group_id: new_template_group_id.value,
  new_content: "",
  new_file_name: "",
  new_file_type: "",
  new_createdon: "",
  new_modifiedon: "",
  new_attachment_id: "",
});
if (!new_template_group_id.value) {
  ElMessage.error("缺失主档模板组!");
} else {
  formData.value.new_template_group_id = new_template_group_id.value;
}
var fileList = ref([]);
var dialogCodeVisible = ref(false);
var previeworedit = ref(true);
var isrender = ref(false);
var codeString = ref("");
const activeCollapseNames = ref(["1"]);

onMounted(() => {
  loadData();
});

/**加载数据 */
function loadData() {
  if (id.value) {
    loading.value = true;
    req
      .get(`/api/new_template_content/get/?id=${id.value}`)
      .then((res) => {
        loading.value = false;
        formData.value = res.data;
      })
      .catch((err) => {
        loading.value = false;
        console.error(err);
      });
  }
}

/**保存 */
function save() {
  loading.value = true;
  req
    .post("/api/new_template_content/save/", formData.value)
    .then((res) => {
      loading.value = false;
      id.value = res.data;
      loadData();
    })
    .catch((err) => {
      loading.value = false;
      console.error(err);
    });
}

function create() {
  id.value = "";
  formData.value = {
    new_template_contentid: id.value,
    new_template_group_id: new_template_group_id.value,
    new_content: "",
    new_file_name: "",
    new_file_type: "",
    new_createdon: "",
    new_modifiedon: "",
    new_attachment_id: "",
  };
  fileList.value = [];
}

/**删除 */
function del() {
  loading.value = true;
  req
    .post("/api/new_template_content/delete/", [id.value])
    .then((res) => {
      loading.value = false;
      back();
    })
    .catch((err) => {
      loading.value = false;
      console.error(err);
    });
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

/**生成当前文档并预览 */
function render() {
  loading.value = true;
  req
    .get(`/api/templaterender/template_content/?id=${id.value}`)
    .then((res) => {
      loading.value = false;
      codeString.value = res.data;
      isrender.value = true;
      dialogCodeVisible.value = true;
    })
    .catch((err) => {
      loading.value = false;
      ElMessage.error(err);
    });
}

/**预览当前模板 */
function preview() {
  loadingDialog.value = true;
  req
    .get(`/api/templaterender/preview_template_content/?id=${id.value}`)
    .then((res) => {
      loadingDialog.value = false;
      codeString.value = res.data.replace(/\n/g, "<br/>");
      previeworedit.value = true;
      isrender.value = false;
      dialogCodeVisible.value = true;
    })
    .catch((err) => {
      loadingDialog.value = false;
      ElMessage.error(err);
      // 报错后转编辑
      editcode();
      isrender.value = false;
      dialogCodeVisible.value = true;
    });
}

/**编辑代码 */
function editcode() {
  loadingDialog.value = true;
  req
    .get(`/api/templaterender/edit_template_content/?id=${id.value}`)
    .then((res) => {
      loadingDialog.value = false;
      codeString.value = res.data; //.replace(/\n/g, "<br/>");
      previeworedit.value = false;
    })
    .catch((err) => {
      loadingDialog.value = false;
      ElMessage.error(err);
    });
}

/**保存代码 */
function savecode() {
  loadingDialog.value = true;
  req
    .post("/api/new_template_content/savecode/", {
      content: codeString.value,
      id: id.value,
    })
    .then((res) => {
      loadingDialog.value = false;
      ElMessage.success("保存成功");
    })
    .catch((err) => {
      loadingDialog.value = false;
      ElMessage.error(err);
    });
}
</script>

<style scoped>
.my-header {
  display: flex;
  flex-direction: row;
  justify-content: end;
  gap: 16px;
}
</style>
