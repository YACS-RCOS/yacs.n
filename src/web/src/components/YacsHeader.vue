<script setup>
import {getDefaultSemester} from "../plugins/axios/apis";
import {currentSemester, semesters} from "../store";

</script>

<template>
  <el-page-header @back="" icon="">
    <template #title>YACS</template>
    <template #content>
      <el-menu mode="horizontal" ref="menu" :ellipsis="false" :default-active="this.$route.path">
        <el-select v-model="currentSemester" class="yacs-header__dd">
          <el-option v-for="(_, key) in semesters" :label="key" :value="key" />
        </el-select>
        <el-menu-item @click="$router.push({path: '/'})" index="/">schedule</el-menu-item>
        <el-menu-item @click="$router.push({path: '/explore'})" index="/explore">explore</el-menu-item>
      </el-menu>
    </template>
  </el-page-header>
</template>

<style scoped>
:deep(.el-menu--horizontal) {
  border: 0;
}

:deep(.el-page-header__title) {
  font-size: 24px;
  font-weight: bold;
  color: gray;
  line-height: 59px;
}

.yacs-header__dd {
  display: inline-flex;
  justify-content: center;
  align-items: center;
}
</style>