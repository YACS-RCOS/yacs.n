<script setup>
import YacsHeader from './components/YacsHeader.vue'
import YacsSideBar from './components/YacsSideBar.vue'
</script>

<template>
  <el-container>
    <el-header>
      <yacs-header v-if="true"></yacs-header>
    </el-header>
    <el-container>
      <el-aside v-if="this.$route.meta.sideBar" width="30%">
        <yacs-side-bar></yacs-side-bar>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<style>
body {
  margin: 0;
  font-family: 'Roboto';
}

* {
  outline: none;
}

.el-aside {
  padding: 30px;
}

.el-header {
  border-bottom: #e6e6e6;
  box-shadow: 0 15px 25px 0 rgba(0, 0, 0, .15);
}
</style>
