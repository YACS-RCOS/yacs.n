<template>
  <div>
    <el-form ref="form" :model="formData">
      <el-form-item label="File">
        <input type="file" name="file" @change="handler" />
      </el-form-item>
      <el-form-item label="Make Public">
        <input type="checkbox" name="file" v-model="formData.isPubliclyVisible" />
      </el-form-item>
      <el-form-item>
        <el-button @click="submitUpload">submit</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import client from "../../plugins/axios"
import { reactive, ref, watchEffect } from "vue"
const form = ref(null)
const formData: {
  file: File | null,
  isPubliclyVisible: boolean
} = reactive({
  file: null,
  isPubliclyVisible: true
})
const handler = (a: any) => {
  formData.file = a.target.files[0] || null
}
const submitUpload = () => {
  const submission = new FormData()
  submission.set('file', formData.file!)
  submission.set('isPubliclyVisible', formData.isPubliclyVisible.toString())
  client.post('/bulkCourseUpload', submission)
}
</script>

<style scoped>

</style>