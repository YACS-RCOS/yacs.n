<script setup>
import { /*currentSelections as */displayedSelections, selections } from "../utils/scheduler";

const test = () => {
  // console.log('hi')
}
</script>

<template>
  <div>
    <el-collapse>
      <el-collapse-item v-for="(course, name, index) in displayedSelections" :name="index">
        <template #title>
          {{ name }}
          <div style="width: 15px; height: 15px; position:absolute; right: 30px; line-height: normal" @click.prevent="test">x</div>
        </template>
        <div v-for="(section, crn) in course.sections">
          <el-checkbox v-model="section.isSelected"></el-checkbox>
          {{ crn }}
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<style scoped>

</style>