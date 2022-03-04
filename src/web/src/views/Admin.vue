
<template>
  <el-container>
    <el-header>Admin Panel</el-header>
    <hr />
    <br />

    <el-button type="text" @click="uploadVisible = true" class="option">
      Import Courses via CSV
    </el-button>

    <el-button type="text" @click="editSemesterVisible = true" class="option">
      Edit Semesters
    </el-button>

    <el-button type="text" @click="setDefaultVisible = true" class="option">
      Set Default Semester
    </el-button>

    <el-dialog
      v-model="uploadVisible"
      title="Import Courses via CSV"
      width="40%"
    >
      <component :is="UploadCSV" />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editSemesterVisible = false">
            Cancel
          </el-button>
          <el-button type="primary" @click="uploadVisible = false">
            OK
          </el-button>
        </span>
      </template>
    </el-dialog>
  
    <el-dialog
      v-model="editSemesterVisible"
      title="Assign Semetser Part Name to Date Ranges"
      width="40%"
    >
      <component :is="EditSemesters" />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editSemesterVisible = false">
            Cancel
          </el-button>
          <el-button type="primary" @click="editSemesterVisible = false">
            OK
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="setDefaultVisible"
      title="Set Default Semester"
      width="40%"
    >
      <component :is="SetDefault" />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="setDefaultVisible = false">
            Cancel
          </el-button>
          <el-button type="primary" @click="setDefaultVisible = false">
            OK
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Footer of Admin Panel -->
    <el-footer>
      <el-button type="info" href="/">Go back home</el-button>
    </el-footer>

  </el-container>

</template>

<script setup>
import UploadCSV from "../views/UploadCSV.vue";
import EditSemesters from "../views/EditSemesters.vue";
import SetDefault from "../views/SetDefault.vue";

import { ref } from 'vue'
import { uploadCsv } from '../plugins/axios/apis'

const uploadVisible = ref(false)
const editSemesterVisible = ref(false)
const setDefaultVisible = ref(false)

</script>


<style scoped>
.el-header {
  text-align: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  line-height: 60px;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}

.option {
  font-size: 16px;
  margin-top: 10px;
}

.file {
  margin-right: 10px;
}

.description {
  font-size: 16px;
  margin-bottom: 10px;
}

.el-footer {
  justify-content: center;
  text-align: center;
  margin-top: 16px;
}
</style>