<script lang="ts" setup>
import { reactive } from "vue"

const tabs = reactive([{
  label: "schedule 1",
  schedule: []
}])
</script>

<template>
  <el-tabs tab-position="right" type="card">
    <el-tab-pane label="Nav">User</el-tab-pane>
    <!--    <el-tab-pane label="Role">Role</el-tab-pane>-->
    <el-tab-pane closable label="Selected">Config</el-tab-pane>
  </el-tabs>
  <el-button @click="">+</el-button>
</template>

<style scoped>

</style>