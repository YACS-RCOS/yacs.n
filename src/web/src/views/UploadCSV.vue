
<template>
  <el-container>
    <el-main>
      <div class="description">
        Import Course Data
      </div>
      <el-checkbox v-model="isPubliclyVisible" style="margin-bottom:5px">Make Public</el-checkbox>

      <el-upload ref="uploadRef" action="null" :limit="1" :on-exceed="handleExceed" :auto-upload="false">
        <template #trigger>
          <el-button class="file">Select File</el-button>
        </template>
        
        <el-button 
          class="ml-3" 
          type="success" 
          @click="submitUpload"
          :loading="isLoading"
          >
          Upload CSV file
        </el-button>
      </el-upload>

      <template v-if="isSuccessful">
        <el-alert title="Uploaded Successfully" type="success"/>
      </template>

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
let isLoading = false
let isSuccessful = false

const handleExceed = (files) => {
  uploadRef.value.clearFiles()
  uploadRef.value.handleStart(files[0])
}

const submitUpload = () => {
  if (!isLoading) {
    isLoading = true
    const formData = new FormData()
    formData.set('file', uploadRef.value.uploadFiles[0].raw)
    formData.set('isPubliclyVisible', isPubliclyVisible)
    uploadCsv(formData)
      .then((response) => {
        console.log(response)
        // Axios will only enter this block if the status code is 2xx,
        // so handle errors for catch block. https://stackoverflow.com/questions/49967779/axios-handling-errors
        isLoading = false
        isSuccessful = true
      })
      .catch((error) => {
        console.log(error.response)
        isLoading = false
      })
  }
  isLoading = false

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