
<template>
  <el-container>
    <el-main v-loading="loading">
      <div class="description">
        Import Course Data
      </div>
      <el-checkbox v-model="isPubliclyVisible" style="margin-bottom:5px">Make Public</el-checkbox>

      <el-upload ref="uploadRef" action="null" :limit="1" :on-exceed="handleExceed" :auto-upload="false">
        <template #trigger>
          <el-button class="file">Select File</el-button>
        </template>
        
        <el-button class="ml-3" type="success" @click="submitUpload">
          Upload CSV file
        </el-button>
      </el-upload>

      <el-divider></el-divider>

      <div class="description">
        For more info, see: 
        <a href="#">http://help.com</a>
        (show github link for more docs later)
      </div>

    </el-main>
  </el-container>
</template>

<script setup>

import { ref } from 'vue'
import { uploadCsv } from '../plugins/axios/apis'

const uploadRef = ref(null)
let isPubliclyVisible = true
let loading = false

const handleExceed = (files) => {
  uploadRef.value.clearFiles()
  uploadRef.value.handleStart(files[0])
}

const submitUpload = () => {
  if (!loading) {
    console.log(uploadRef.value)
    const formData = new FormData()
    formData.set('file', uploadRef.value.uploadFiles[0].raw)
    formData.set('isPubliclyVisible', isPubliclyVisible)
    loading = true
    uploadCsv(formData)
  }
  loading = false

}
</script>

<style scoped>

.file {
  margin-right: 10px;
}

.description {
  font-size: 16px;
  margin-bottom: 10px;
}

</style>