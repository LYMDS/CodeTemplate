<template>
  <div>
    <el-table
      ref="tableRef"
      :data="tableData"
      style="width: 100%"
      row-key="dataparameterid"
    >
      <el-table-column type="selection" width="40" />
      <el-table-column prop="name" label="参数名" width="180" />
      <el-table-column prop="desc" label="参数描述" width="180" />
      <el-table-column prop="value" label="参数值" width="580">
        <template #default="scope">
          <el-input
            v-model="scope.row.value"
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
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
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

const props = defineProps(["nature", "datadriverid", "templateparamid"]);
// nature 1 => 驱动基数参数
// nature 2 => 驱动执行参数
const router = useRouter();
// 表格数据
const tableData = ref([]);
// 源数据
const originData = ref([]);
const tableRef = ref(null);

onMounted(() => {
  load();

  watch(
    () => props.datadriverid,
    (newVal) => {
      load();
    }
  );
  watch(
    () => props.templateparamid,
    (newVal) => {
      load();
    }
  );
});



function load() {
  debugger;
  if (props.datadriverid && props.nature == 1) {
    req
      .get(`/api/dataparameter/getlistbydatadriverid/?id=${props.datadriverid}`)
      .then((res) => {
        tableData.value = res.data;
        DeepCopyTableData();
      })
      .catch((err) => {
        ElMessage.error(err);
      });
  }
  if (props.templateparamid && props.nature == 2) {
    req
      .get(`/api/dataparameter/getlistbytemplateparamid/?id=${props.templateparamid}`)
      .then((res) => {
        tableData.value = res.data;
        DeepCopyTableData();
      })
      .catch((err) => {
        ElMessage.error(err);
      });
  }
}

function DeepCopyTableData() {
  originData.value = JSON.parse(JSON.stringify(tableData.value));
}

const getLabel = (value) => {
  const option = typeOptions.value.find((opt) => opt.value === value);
  return option ? option.label : "";
};

/**批量保存 */
function batchSave() {
  if (tableData.value && tableData.value.length > 0) {
    var changeData = tableData.value.filter((r) =>
      checkRealChange(
        r,
        originData.value.find(
          (o) => o.datadriverid == r.datadriverid
        ),
        ["name", "value"]
      )
    );
    if (changeData && changeData.length > 0) {
      req
        .post("/api/dataparameter/batchsave/", tableData.value)
        .then((res) => {
          ElMessage.success("保存成功");
          load();
        })
        .catch((err) => {
          ElMessage.error(err);
        });
    } else {
      ElMessage.error("没有数据需要保存");
    }
  } else {
    ElMessage.error("没有数据需要保存");
  }
}

/**检查真实的脏数据
 * changeList 可能发生更改的字段
 */
function checkRealChange(item, originItem, changeList) {
  if (!originItem) return true; // 新增数据
  var change = false;
  if (!changeList || changeList.length == 0) {
    alert("脏数据列表配置错误!");
  }
  changeList.forEach((c) => {
    change = change || item[c] != originItem[c];
  }); // 是否有 有效字段被修改
  return change;
}

defineExpose({
  load,
  props
});
</script>