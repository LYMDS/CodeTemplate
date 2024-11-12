<template>
  <el-container>
    <el-header>
      <el-button type="primary" round @click="save">保存</el-button>
      <el-button type="success" round @click="create">新建</el-button>
      <el-button type="danger" round @click="del">删除</el-button>
      <el-button type="success" round @click="render">生成</el-button>
      <el-button type="danger" round @click="preview">预览模板</el-button>
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
      <el-table
        v-show="id"
        ref="tableRef"
        :data="tableData"
        style="width: 100%"
        @row-dblclick="dblclick"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="new_name" label="参数名" width="180" />
        <el-table-column prop="new_type" label="参数类型" width="180" >
          <template #default="scope">
            {{ getLabel(scope.row.new_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="new_value" label="参数值" width="500" />
        <!-- <el-table-column prop="new_createdon" label="创建时间" width="180" />
        <el-table-column prop="new_modifiedon" label="修改时间" width="180" /> -->
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
    <el-dialog v-model="dialogCodeVisible" :show-close="false" width="70%">
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
var dialogCodeVisible = ref(false);
var previeworedit = ref(true);
var isrender = ref(false);
var codeString = ref("");
var typeOptions = ref([
    {
      label: "文本",
      value: 1
    },
    {
      label: "对象",
      value: 2
    },
    {
      label: "列表",
      value: 3
    },
  ])
  const getLabel = (value) => {
      const option = typeOptions.value.find(opt => opt.value === value);
      return option ? option.label : '';
    }
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
    req
      .get(`/api/new_template_param/getlistbycontentid/?id=${id.value}`)
      .then((res) => {
        console.log("res", res.data);
        tableData.value = res.data;
      })
      .catch((err) => {
        ElMessage.error(err);
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
  tableData.value = [];
  fileList.value = [];
}

/**删除 */
function del() {
  req
    .post("/api/new_template_content/delete/", [id.value])
    .then((res) => {
      console.log("res", res);
      back();
    })
    .catch((err) => {
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
      new_template_code_id: id.value,
    },
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
      new_template_code_id: id.value,
    },
  });
}

/**生成当前文档并预览 */
function render() {
  req
    .get(`/api/templaterender/template_content/?id=${id.value}`)
    .then((res) => {
      // console.log("/api/templaterender/template_content/=>res", res.data);
      codeString.value = res.data;
      isrender.value = true;
      dialogCodeVisible.value = true;
    })
    .catch((err) => {
      ElMessage.error(err);
    });
}

/**预览当前模板 */
function preview() {
  req
    .get(`/api/templaterender/preview_template_content/?id=${id.value}`)
    .then((res) => {
      // console.log("/api/templaterender/template_content/=>res", res.data);
      codeString.value = res.data.replace(/\n/g, "<br/>");
      previeworedit.value = true;
      isrender.value = false;
      dialogCodeVisible.value = true;
    })
    .catch((err) => {
      ElMessage.error(err);
      // 报错后转编辑
      editcode();
      dialogCodeVisible.value = true;
    });
}

/**编辑代码 */
function editcode() {
  req
    .get(`/api/templaterender/edit_template_content/?id=${id.value}`)
    .then((res) => {
      codeString.value = res.data; //.replace(/\n/g, "<br/>");
      previeworedit.value = false;
    })
    .catch((err) => {
      ElMessage.error(err);
    });
}

/**保存代码 */
function savecode() {
  req.post("/api/new_template_content/savecode/", {
    content: codeString.value,
    id: id.value
  }).then(res => {
    ElMessage.success("保存成功");
  }).catch(err => {
    ElMessage.error(err);
  })

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
