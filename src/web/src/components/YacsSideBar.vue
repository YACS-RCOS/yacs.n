<script setup>
import {ref, reactive, watchEffect} from 'vue'
import {getCourses} from "../plugins/axios/apis";
import {currentSemester, semester, selections} from "../store";
import {filterCourses} from "../utils/common";

import YacsSelectionPanel from '../components/YacsSelectionPanel.vue'

const defaultTab = ref({label: 'Course Search', name: '#default', isActive: true})
const activeName = ref('#default')

const searchParam = reactive({
  input: '',
  department: null
})

const searchResult = ref([])

watchEffect(() => {
  if (!currentSemester.value || !semester.value) return
  getCourses(currentSemester.value, searchParam.department).then(res => {
    searchResult.value = filterCourses(res).map((course) => semester.value[course.name])
    count.value = Math.min(searchResult.value.length, 20)
  })
})

const count = ref(0)
const load = () => {
  count.value += 10
}

const toggleSelection = (obj, value) => {
  if (value) {
    selections[obj.name] = Object.keys(semester.value[obj.name].sections)
  } else {
    delete selections[obj.name]
  }
  for (let section in obj.sections) {
    obj.sections[section].isSelected = value
  }
}

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
            <el-input v-model="searchParam.department"></el-input>
          </el-form-item>
        </el-form>
        <div v-if="searchResult.length">
          <el-scrollbar height="700px">
            <ul v-infinite-scroll="load" class="yacs-infinite-list">
              <li v-for="i in count" class="yacs-infinite-list-item">
                <el-checkbox v-model="searchResult[i-1].isSelected"
                             @change="toggleSelection(searchResult[i-1], $event)"></el-checkbox>
                {{ searchResult[i - 1].name }}
                {{ searchResult[i - 1].title }}
              </li>
            </ul>
          </el-scrollbar>
        </div>
      </el-tab-pane>
      <el-tab-pane label="Schedule">
        <yacs-selection-panel></yacs-selection-panel>
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

.yacs-infinite-list {
  padding: 0;
  margin: 0;
  list-style: none;
}

.yacs-infinite-list .yacs-infinite-list-item {
  display: flex;
  height: 100px;
  background: var(--el-color-primary-light-9);
  margin: 10px 0;
  color: var(--el-color-primary);
}
</style>