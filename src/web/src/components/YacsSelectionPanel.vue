<script setup>
import {currentSemester} from "../utils/core/semester";
import { displayedSelections, selections, toggleSection } from "../utils/core/selection";
</script>

<template>
  <div>
    <el-collapse>
      <el-collapse-item v-for="(crns, courseName, index) in displayedSelections" :name="index">
        <template #title>
          {{ courseName }}
          <div style="width: 15px; height: 15px; position:absolute; right: 30px; line-height: normal" @click.prevent="test">x</div>
        </template>
        <div v-for="(section, crn) in currentSemester.courses[courseName].sections">
          <el-checkbox :model-value="crns.includes(crn)" @change="toggleSection(currentSemester.courses[courseName], crn, $event)"></el-checkbox>
          {{ crn }}
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<style scoped>

</style>