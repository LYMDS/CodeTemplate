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
          <el-form-item label="参数名">
            <el-input v-model="formData.new_name" placeholder="" clearable />
          </el-form-item>
          <el-form-item label="参数类型">
            <!-- <el-input v-model="formData.new_type" placeholder="" clearable /> -->

            <el-select
              v-model="formData.new_type"
              placeholder="选择类型"
              style="width: 240px"
            >
              <el-option
                v-for="item in typeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>

          </el-form-item>
          <el-form-item label="参数值">
            <el-input v-model="formData.new_value" placeholder="" clearable />
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
      </el-main>
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
  var new_template_code_id = ref("");
  
  var formData = ref({
    new_template_paramid: id.value,
    new_name: "",
    new_type: "",
    new_value: "",
    new_template_group_id: new_template_group_id.value,
    new_template_code_id: new_template_code_id.value,
    new_createdon: "",
    new_modifiedon: "",
  });
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
  var tableData = ref([]);
  var fileList = ref([]);
  
  onMounted(() => {
    id.value = router.currentRoute.value.query.id;
    new_template_group_id.value =
      router.currentRoute.value.query.new_template_group_id;
    new_template_code_id.value = 
      router.currentRoute.value.query.new_template_code_id;
    if (!new_template_group_id.value) {
      ElMessage.error("缺失主档模板组!");
    } else {
      formData.value.new_template_group_id = new_template_group_id.value;
    }
    if (!new_template_code_id.value) {
      ElMessage.error("缺失关联模板代码!");
    }else{
      formData.value.new_template_code_id = new_template_code_id.value;
    }
    loadData();
  });
  
  /**加载数据 */
  function loadData() {
    if (id.value) {
      req
        .get(`/api/new_template_param/get/?id=${id.value}`)
        .then((res) => {
          console.log("res", res.data);
          formData.value = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    }
  }
  
  
  /**保存 */
  function save() {
    req
      .post("/api/new_template_param/save/", formData.value)
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
    // id.value = ""
    // formData.value = {
    //   new_template_contentid: id.value,
    //   new_template_group_id: new_template_group_id.value,
    //   new_content: "",
    //   new_file_name: "",
    //   new_file_type: "",
    //   new_createdon: "",
    //   new_modifiedon: "",
    //   new_attachment_id: "",
    // }
    // tableData.value = [];
    // fileList.value = [];
  }
  
  /**删除 */
  function del() {
    req.post("/api/new_template_param/delete/", [id.value]).then(res => {
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
  