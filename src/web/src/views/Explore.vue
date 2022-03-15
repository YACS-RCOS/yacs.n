<script setup>
import {getDepartments} from "../plugins/axios/apis";

getDepartments().then(res => {
  console.log(res)
})
</script>

<template>
  <div>
<!--    <div><el-card></el-card></div>-->
<!--    <div><el-card></el-card></div>-->
  </div>
</template>

<style scoped>

</style>