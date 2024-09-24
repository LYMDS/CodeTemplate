<template>
  <div class="about">
    <h1>This is an about page</h1>
    <el-upload
    v-model:file-list="fileList"
    class="upload-demo"
    action="http://localhost:8008/api/new_attachment/upload/"
    multiple
    :limit="3"
    >
      <el-button type="primary">Click to upload</el-button>
      <template #tip>
        <div class="el-upload__tip">
          jpg/png files with a size less than 500KB.
        </div>
      </template>
    </el-upload>

    <el-button @click="download">点击下载</el-button>
  </div>
  
</template>

<script setup>
import { onMounted, ref } from 'vue'
import req from '../common/interface'
import { useRouter } from "vue-router";
import { RefreshRight } from '@element-plus/icons-vue'
import { ElMessage,ElNotification,ElMessageBox } from 'element-plus';

var attachmentId = ref("39cfdaf35ed811efae58acd564a6cbf4")
const fileList = ref([])

function download() {
  if (attachmentId) {
    
    //req.get(`/api/new_attachment/download/?id=${attachmentId.value}`)
    req.opendownload(`/api/new_attachment/download/?id=${attachmentId.value}`)
  }
}

function aa(content, filename) {
  var a_link = document.createElement('a')
  a_link.download = filename
  a_link.style.display = 'none'

  var blob = new Blob([content])
  a_link.href = URL.createObjectURL(blob)

  document.body.appendChild(a_link)
  a_link.click()
  document.body.removeChild(a_link)
}

</script>

<style>
/* @media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
} */
</style>
