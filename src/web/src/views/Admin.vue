
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
      title="Import Data"
      width="40%"
    >
      <div class="description">
        Input course data as CSV
      </div>

      <el-checkbox v-model="isPubliclyVisible" style="margin-bottom:5px">Make Public</el-checkbox>

      <el-upload ref="uploadRef" action="null" :auto-upload="false">
        <template #trigger>
          <el-button class="file">Select File</el-button>
        </template>
        
        <el-button class="ml-3" type="success" @click="submitUpload">
          Upload CSV file
        </el-button>
      </el-upload>

      <el-divider></el-divider>

      <div>
        For more info, see: 
        <a href="#">http://help.com</a>
        (show github link for more docs later)
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadVisible = false">
            Cancel
          </el-button>
          <el-button type="primary" @click="uploadVisible = false">
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
// import UploadCsv from "@/pages/UploadCsv";
// import EditSemesters from "@/pages/EditSemesters";
// import SetDefault from "@/pages/SetDefault";

import { ref } from 'vue'
import { uploadCsv } from '../plugins/axios/apis'

const uploadVisible = ref(false)
const editSemesterVisible = ref(false)
const setDefaultVisible = ref(false)
const uploadRef = ref(null)
const isPubliclyVisible = ref(false)

const submitUpload = () => {
  // console.log(uploadRef.value)
  const formData = new FormData()
  formData.set('file', uploadRef.value.uploadFiles[0].raw)
  formData.set('isPubliclyVisible', true)
  uploadCsv(formData)
}
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