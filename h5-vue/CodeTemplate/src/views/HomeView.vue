<template>
  <el-container class="el-container-main">
    <el-aside class="el-aside-main" width="150px">
      <el-menu default-active="2" class="el-menu-main" :collapse="isCollapse" @open="handleOpen"
        @close="handleClose" :router="true">
        <el-sub-menu index="1">
          <template #title>
            <el-icon><icon-menu /></el-icon>
            <span>模板</span>
          </template>
          <el-menu-item index="/TemplateGroupList">模版组</el-menu-item>
          <el-menu-item index="/about">关于</el-menu-item>

        </el-sub-menu>

        <el-menu-item index="/">
          <el-icon>
            <setting />
          </el-icon>
          <template #title>设置</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main>
      <router-view>
      </router-view>
    </el-main>
  </el-container>

</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

const isCollapse = ref(false);

onMounted(() => {


})

function handleOpen(key, keyPath) {
  console.log(key, keyPath);
}

function handleClose(key, keyPath) {
  console.log(key, keyPath);
}
</script>

<style scoped>
.el-menu-main {
  height: 100%;
}
.el-aside-main {
  height: 100%;
} 
.el-container-main{
  height: 100%;
}
</style>
