<script setup>
import {ref, watch} from "vue";

const defaultTab = ref({label: 'Course Search', name: '#default', isActive: true})
const activeName = ref('#default')

</script>

<template>
  <div>
    <el-tabs tab-position="right"
             type="card"
             v-model="activeName">
      <el-tab-pane :label="defaultTab.label" :name="defaultTab.name">
        <el-form label-position="top">
          <el-form-item label="Search">
            <el-input></el-input>
          </el-form-item>
          <el-form-item label="Filter Department">
            <el-input></el-input>
          </el-form-item>
        </el-form>
        <div></div>
      </el-tab-pane>
      <el-tab-pane label="Schedule">

      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
:deep(.el-tabs__header).is-right {
  border-bottom: none;
  position: relative;
  padding-bottom: 45px;
}

:deep(.el-tabs--card) > .el-tabs__header .el-tabs__item {
  writing-mode: vertical-lr;
  height: auto;
  padding: 20px 0;
}

:deep(.el-tabs--card) > .el-tabs__header .el-tabs__item.is-active {
  padding: 20px 0;
}

:deep(.el-tabs__new-tab) {
  position: absolute;
  bottom: 0;
}
</style>