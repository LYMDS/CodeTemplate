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
        <el-form-item label="模板名称">
          <el-input v-model="formData.new_name" placeholder="" clearable :spellcheck="false"/>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.new_note" placeholder="" clearable :spellcheck="false"/>
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
        <el-collapse-item title="文件列表" name="1">
          <el-table
            ref="tableRef"
            :data="tableData"
            style="width: 100%"
            @row-dblclick="dblclick"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="new_file_name" label="文件名" width="180" />
            <el-table-column prop="new_content" label="内容" width="180" />
            <el-table-column
              prop="new_file_type"
              label="文件类型"
              width="180"
            />
            <el-table-column
              prop="new_createdon"
              label="创建时间"
              width="180"
            />
            <el-table-column
              prop="new_modifiedon"
              label="修改时间"
              width="180"
            />
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
        </el-collapse-item>
        <el-collapse-item title="参数列表" name="2">
          <ParamEditor :type="1" :id="id" :groupid="id" />
        </el-collapse-item>
      </el-collapse>
    </el-main>
  </el-container>
</template>

<script setup>
import { onMounted, ref } from "vue";
import req from "../common/interface";
import { useRouter } from "vue-router";
import { Plus, RefreshRight } from "@element-plus/icons-vue";
import ParamEditor from "../components/ParamEditor.vue";
const router = useRouter();
var id = ref("");
id.value = router.currentRoute.value.query.id;
var formData = ref({
  new_template_groupid: id.value || "",
  new_name: "",
  new_note: "",
  new_createdon: "",
  new_modifiedon: "",
});
var tableData = ref([]);
const activeCollapseNames = ref(["1"]);

onMounted(() => {
  loadData();
  loadLine();
});

/**加载数据 */
function loadData() {
  if (id.value) {
    req
      .get(`/api/new_template_group/get/?id=${id.value}`)
      .then((res) => {
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
      .get(`/api/new_template_content/getlistbygroupid/?id=${id.value}`)
      .then((res) => {
        tableData.value = res.data;
      })
      .catch((err) => {
        console.error(err);
      });
  }
}

/**保存 */
function save() {
  req
    .post("/api/new_template_group/save/", formData.value)
    .then((res) => {
      id.value = res.data;
      loadData();
    })
    .catch((err) => {
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
  req
    .post("/api/new_template_group/delete/", [id.value])
    .then((res) => {
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

/**路由回退 */
function back() {
  router.back();
}

/**跳转内容明细 */
function dblclick(event) {
  router.push({
    path: "/TemplateContentEdit",
    query: {
      id: event.new_template_contentid,
      new_template_group_id: id.value,
    },
  });
}

/**创建内容明细 */
function createLine() {
  router.push({
    path: "/TemplateContentEdit",
    query: {
      new_template_group_id: id.value,
    },
  });
}
</script>

<style scoped></style>
