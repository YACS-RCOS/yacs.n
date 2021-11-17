<script setup lang="ts">

</script>

<template>
  <el-page-header :icon="null">
    <template #title>YACS</template>
    <template #content>
      <el-menu
        mode="horizontal"
        default-active="1"
        :router="true"
        :ellipsis="false"
      >
        <el-menu-item index="1" route='/'>Schedule</el-menu-item>
        <el-menu-item index="2" route='/explore'>Explore</el-menu-item>
      </el-menu>
    </template>
  </el-page-header>
</template>

<style scoped lang="scss">
.el-page-header {
  line-height: 60px;
  ::v-deep(.el-page-header__content) {
    flex: 1;
  }
  .el-menu--horizontal {
    border: none;
  }
}
</style>