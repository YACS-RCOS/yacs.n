<script setup>
import {getDefaultSemester} from "../plugins/axios/apis";
import {currentSemester, semester, semesters} from "../store";
import {computed, ref, watchEffect} from 'vue'
import {subActivated} from "../utils/scheduler";

const options = ref([])
watchEffect(() => {
  options.value = Object.keys(semesters).map((value) => {
    return {
      label: value,
      value,
      children: semesters[value].sub && semesters[value].sub.slice(1).map(([start, end], index) => ({
        label: (start.getMonth() + 1) + '.' + start.getDate() + '-' + (end.getMonth() + 1) + '.' + end.getDate(),
        value: index + 1
      }))
    }
  })
})

const testing = ref([])

watchEffect(() => {
  if (testing.value.length === 0 && currentSemester.value) {
    testing.value[0] = currentSemester.value
  }
})

watchEffect(() => {
  currentSemester.value = testing.value[0]
  subActivated.value = testing.value[1] || 0
})
</script>

<template>
  <el-page-header @back="" icon="">
    <template #title>YACS</template>
    <template #content>
      <el-menu mode="horizontal" ref="menu" :ellipsis="false" :default-active="this.$route.path">
<!--        <el-select v-model="currentSemester" class="yacs-header__dd">
          <el-option v-for="(_, key) in semesters" :label="key" :value="key" />
        </el-select>-->
        <el-cascader class="yacs-header__dd" v-model="testing" :options="options"></el-cascader>
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