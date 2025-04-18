<template>
  <el-container v-loading="loading">
    <el-header>
      <el-button type="primary" round @click="create">新建</el-button>
      <el-button type="primary" round @click="save">保存</el-button>
      <el-button type="danger" round @click="del">删除</el-button>
      <el-button type="danger" round @click="back">返回</el-button>
    </el-header>
    <el-main>
      <el-form :model="formData" label-position="top">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="驱动器名称">
              <el-input
                v-model="formData.name"
                placeholder=""
                clearable
                :spellcheck="false"
              />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="驱动器说明">
              <el-input
                type="textarea"
                autosize
                v-model="formData.desc"
                placeholder=""
                clearable
                :spellcheck="false"
              />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="创建时间">
              <el-date-picker
                v-model="formData.createdon"
                type="datetime"
                placeholder="Empty"
                disabled
              />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="修改时间">
              <el-date-picker
                v-model="formData.modifiedon"
                type="datetime"
                placeholder="Empty"
                disabled
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="类型">
              <el-select
                v-model="formData.type"
                placeholder="请选择驱动器"
                style="width: 300px"
                :disabled="id"
              >
                <el-option
                  v-for="item in typeOptionSet"
                  :key="item.value"
                  :label="item.name"
                  :value="item.value"
                >
                  <span style="float: left">{{ item.name }}</span>
                  <span
                    style="
                      float: right;
                      color: var(--el-text-color-secondary);
                      font-size: 13px;
                    "
                  >
                    {{ item.value }}
                  </span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-collapse v-model="activeCollapseNames">
        <el-collapse-item title="参数列表" name="1">
          <DataParameterEditor ref="dataparametereditorRef" :nature="1" :datadriverid="id" ></DataParameterEditor>
        </el-collapse-item>
      </el-collapse>
    </el-main>
  </el-container>
</template>

<script setup>
import { onMounted, ref } from "vue";
import req from "../common/interface";
import { useRouter } from "vue-router";
import { ElMessage, ElNotification, ElMessageBox } from "element-plus";
import { Plus, RefreshRight } from "@element-plus/icons-vue";
import DataParameterEditor from "../components/DataParameterEditor.vue";
var loading = ref(false);
const router = useRouter();
var id = ref("");

var formData = ref({
  datadriverid: id.value,
  name: "",
  desc: "",
  type: "",
  createdon: "",
  modifiedon: "",
});
var tableData = ref([]);
var typeOptionSet = ref([]);
const activeCollapseNames = ref(["1"]);
const dataparametereditorRef = ref(null);
id.value = router.currentRoute.value.query.id;
getTypeOptionSet();
onMounted(() => {
  loadData();
});

/**加载数据 */
function loadData() {
  if (id.value) {
    loading.value = true;
    req
      .get(`/api/datadriver/get/?id=${id.value}`)
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

/**获取驱动类型列表 */
function getTypeOptionSet() {
  req
    .get("/api/datadriver/gettypeoptionset/")
    .then((res) => {
      typeOptionSet.value = res.data;
    })
    .catch((err) => {
      ElMessage.error(err);
    });
}

/**保存 */
function save() {
  loading.value = true;
  req
    .post("/api/datadriver/save/", formData.value)
    .then((res) => {
      loading.value = false;
      id.value = res.data;
      ElMessage.success("保存成功!");
      if (router.currentRoute.value.name == "DataDriverCreate") {
        router.push({
          name: "DataDriverEdit",
          query: { id: id.value },
        });
      } else {
        loadData();
      }
      
      // dataparametereditorRef.value.props.datadriverid = id.value;
      // dataparametereditorRef.value.load();
      
    })
    .catch((err) => {
      console.error(err);
    });
}

function create() {
  router.push("/DataDriverCreate");
}

/**删除 */
function del() {
  loading.value = true;
  req
    .post("/api/datadriver/delete/", [id.value])
    .then((res) => {
      loading.value = false;
      back();
    })
    .catch((err) => {
      loading.value = false;
      console.error(err);
    });
}

/**路由回退 */
function back() {
  router.back();
}
</script>

<style scoped></style>
