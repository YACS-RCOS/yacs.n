<template>
  <el-upload ref="uploadRef" action="null" :auto-upload="false">
    <template #trigger>
      <el-button type="primary">select file</el-button>
    </template>
    <el-button class="ml-3" type="success" @click="submitUpload">
      upload to server
    </el-button>
  </el-upload>
</template>

<script setup>
import {ref} from 'vue'
import {uploadCsv} from '../plugins/axios/apis'

const uploadRef = ref(null)

const submitUpload = () => {
  // console.log(uploadRef.value)
  const formData = new FormData()
  formData.set('file', uploadRef.value.uploadFiles[0].raw)
  formData.set('isPubliclyVisible', true)
  uploadCsv(formData)
}

// uploadCsv('Spring 2022')
</script>

<style scoped>

</style>