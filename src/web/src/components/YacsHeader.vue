<script setup>
import {currentSemesterName, currentSemester, semesters, subSemester} from "../utils/core/semester";
import {computed, ref, watchEffect} from 'vue'

const getLabel = ([s, e]) => {
  return (s.getMonth() + 1) + '.' + s.getDate() + ' - ' + (e.getMonth() + 1) + '.' + e.getDate()
}

const options = ref([])
watchEffect(() => {
  options.value = Object.keys(semesters).map((value) => {
    return {
      label: value,
      value,
      children: semesters[value].sub && [
        {
          label: getLabel(semesters[value].sub.first),
          value: 'first'
        }, {
          label: getLabel(semesters[value].sub.second),
          value: 'second'
        }
      ]
    }
  })
})

const testing = ref([])

watchEffect(() => {
  // try init
  if (testing.value.length === 0 && currentSemesterName.value) {
    testing.value[0] = currentSemesterName.value
  }
})

watchEffect(() => {
  currentSemesterName.value = testing.value[0]
  subSemester.value = testing.value[1] || 'full'
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