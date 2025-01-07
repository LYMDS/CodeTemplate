<template>
  <div>
    <el-table
      v-show="id"
      ref="tableRef"
      :data="tableData"
      style="width: 100%"
      @row-dblclick="dblclick"
      :row-class-name="tableRowClassName"
      row-key="new_template_paramid"
    >
      <el-table-column type="selection" width="40"/>
      <el-table-column type="expand" width="40">
        <template #default="scope">
          <div>
          <el-input
            type="textarea"
            v-model="scope.row.new_value"
            placeholder=""
            clearable
            style="width: 100%"
            :spellcheck="false"
          ></el-input>
          <!-- v-model="scope.row.new_value" -->
        </div>
        </template>
      </el-table-column>
      <el-table-column
        v-if="props.type == 1"
        prop="new_file_name"
        label="所属文件"
        width="100"
      />
      <el-table-column prop="new_name" label="参数名" width="180">
        <template #default="scope">
          <el-input
            v-model="scope.row.new_name"
            placeholder=""
            clearable
            :spellcheck="false"
            required
          ></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="new_type" label="参数类型" width="180">
        <template #default="scope">
          <el-select
            v-model="scope.row.new_type"
            placeholder="选择类型"
            style="width: 150px"
          >
            <el-option
              v-for="item in typeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column prop="new_value" label="参数值" width="580">
        <template #default="scope">
          <el-input
            v-model="scope.row.new_value"
            placeholder=""
            clearable
            style="width: 550px"
            :spellcheck="false"
          ></el-input>
        </template>
      </el-table-column>

      <el-table-column align="right">
        <template #header>
          <el-button
            size="small"
            :icon="Finished"
            type="primary"
            circle
            @click="batchSave"
          ></el-button>
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
          <el-button
            size="small"
            :icon="Delete"
            type="danger"
            circle
            @click="handleDelete"
          >
          </el-button>
        </template>
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
            Edit
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
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

const props = defineProps(["type", "id", "groupid"]);
// type 1 => 模板级全局参数
// type 2 => 文件级局部参数
const router = useRouter();
// 表格数据
const tableData = ref([]);
// 源数据
const originData = ref([]);
const tableRef = ref(null);
const tableRowClassName = ({ row, rowIndex }) => {
  if (row.new_template_code_id) {
    return "local-parameters";
  } else {
    return "global-parameters";
  }
};
var typeOptions = ref([
  {
    label: "文本",
    value: 1,
  },
  {
    label: "对象",
    value: 2,
  },
  {
    label: "列表",
    value: 3,
  },
]);

onMounted(() => {
  load();
});

function load() {
  if (props.id && props.type == 1) {
    req
      .get(`/api/new_template_param/getlistbygroupid/?id=${props.id}`)
      .then((res) => {
        tableData.value = res.data;
        DeepCopyTableData();
      })
      .catch((err) => {
        ElMessage.error(err);
      });
  }
  if (props.id && props.type == 2) {
    req
      .get(`/api/new_template_param/getlistbycontentid/?id=${props.id}`)
      .then((res) => {
        tableData.value = res.data;
        DeepCopyTableData();
      })
      .catch((err) => {
        ElMessage.error(err);
      });
  }
  
}

function DeepCopyTableData(){
  originData.value = JSON.parse(JSON.stringify(tableData.value))
}

const getLabel = (value) => {
  const option = typeOptions.value.find((opt) => opt.value === value);
  return option ? option.label : "";
};

/**刷新 */
function refreshLine() {
  load();
}

/**批量保存 */
function batchSave() {
  if (tableData.value && tableData.value.length > 0) {
    var changeData = tableData.value.filter(r => checkRealChange(r, 
    originData.value.find(o => o.new_template_paramid == r.new_template_paramid), 
    ["new_name", "new_type", "new_value"]));
    if (changeData && changeData.length > 0){
      req
      .post("/api/new_template_param/batchsave/", tableData.value)
      .then((res) => {
        ElMessage.success("保存成功");
        refreshLine();
      })
      .catch((err) => {
        ElMessage.error(err);
      });
    }
    else{
      ElMessage.error("没有数据需要保存");
    }
  }
  else{
      ElMessage.error("没有数据需要保存");
    }
}

function handleDelete() {
  const selectionRows = tableRef.value.getSelectionRows();
  if (selectionRows.length > 0) {
    req
      .post(
        "/api/new_template_param/delete/",
        selectionRows.map((s) => s.new_template_paramid)
      )
      .then((res) => {
        ElMessage.success("删除成功");
        load();
      })
      .catch((err) => {
        ElMessage.error(err);
      });
  }
}

function createLine() {
  tableData.value.push({
    new_createdon: "",
    new_modifiedon: "",
    new_name: "",
    new_template_code_id: props.type == 2 ? props.id : "",
    new_template_group_id: props.type == 1 ? props.id : props.groupid,
    new_template_paramid: "",
    new_type: 1,
    new_value: "",
  });
}

/**跳转内容明细 */
function dblclick(event) {
  router.push({
    path: "/TemplateParamEdit",
    query: {
      id: event.new_template_paramid,
      new_template_group_id: event.new_template_group_id,
      new_template_code_id: event.new_template_code_id,
    },
  });
}

/**跳转内容明细 */
function handleEdit(index, event) {
  dblclick(event);
}

/**检查真实的脏数据
 * changeList 可能发生更改的字段
 */
function checkRealChange(item, originItem, changeList) {
  if (!originItem) return true; // 新增数据
    var change = false;
    if (!changeList || changeList.length == 0) { alert("脏数据列表配置错误!"); }
    changeList.forEach(c => {
      change = change || item[c] != originItem[c];
    }) // 是否有 有效字段被修改
    return change;
}

</script>
<style>
.el-table .local-parameters {
}
.el-table .global-parameters {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
