
<template>
  <el-container>
    <el-main>
      <div class="description">
        Import Course Data
        <el-icon class="icon"><folder-add /></el-icon>
      </div>
      <div>
        <el-checkbox v-model="isPubliclyVisible" style="margin-bottom:5px">Make Public</el-checkbox>
        <div style="font-size: 20px">
          <!-- Since svg icons do not carry any attributes by default -->
          <!-- You need to provide attributes directly -->
          <view style="width: 1em; height: 1em; margin-right: 8px" />
        </div>
      </div>

      <el-upload 
        ref="uploadRef" 
        action="null" 
        :limit="1" 
        :on-exceed="handleExceed" 
        :auto-upload="false"
        >
        <template #trigger>
          <el-button class="file">Select File</el-button>
        </template>
        
        <el-button 
          class="ml-3" 
          type="success" 
          @click="onSubmit"
          :loading="isLoading"
          >
          Upload CSV file
        </el-button>
      </el-upload>

      <template v-if="isSuccessful">
        <el-alert title="Uploaded Successfully" type="success" show-icon/>
      </template>

      <template v-if="isFailed">
        <el-alert title="Upload Failed" type="error" show-icon/>
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

<script>

import { ref } from 'vue'
import { uploadCsv } from '../plugins/axios/apis'

export default {
  name: "UploadCsv",
  data() {
    return {
      uploadRef: ref(null),
      isPubliclyVisible: true,
      isLoading: false,
      isSuccessful: false,
      isFailed: false,
    };
  },
  methods: {
    onSubmit() {
      if (!this.isLoading) {
        const formData = new FormData();
        formData.set('file', this.$refs.uploadRef.uploadFiles[0].raw);
        formData.set('isPubliclyVisible', this.isPubliclyVisible);
        this.isLoading = true;
        uploadCsv(formData)
          .then((response) => {
            console.log(response);
            // Axios will only enter this block if the status code is 2xx,
            // so handle errors for catch block. https://stackoverflow.com/questions/49967779/axios-handling-errors
            this.isLoading = false;
            this.isSuccessful = true;
          })
          .catch((error) => {
            console.log(error.response);
            this.isLoading = false;
            this.isFailed = true;
          });
      }
      this.isSuccessful = false;
      this.isFailed = false;
    },
    handleExceed(files) {
      this.$refs.uploadRef.clearFiles();
      this.$refs.uploadRef.handleStart(files[0]);
    }
  }
}
</script>

<style scoped>

.file {
  margin-right: 10px;
}

.description {
  font-size: 16px;
  margin-bottom: 10px;
  display: inline-block;
}

.icon {
  vertical-align: bottom;
}

</style>