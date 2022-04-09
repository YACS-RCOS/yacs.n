
<template>
  <el-container>
    <el-main>
      <div class="description">
        Set Default Semester
      </div>

      <el-select v-model="semester" class="m-2" placeholder="Select" size="large">
        <el-option
          v-for="sem in semesterOptions"
          :key="sem.value"
          :value="sem.text"
        >
          {{ sem.text }}
        </el-option>
      </el-select>

      <br />

      <el-button 
        class="submit" 
        type="warning" 
        @click="onUpdate"
        :loading = isLoading
        >
        Submit
      </el-button>

      <template v-if="isSuccessful">
        <el-alert title="Submitted Successfully" type="success" show-icon/>
      </template>

      <template v-if="isFailed">
        <el-alert title="Submit Failed" type="error" show-icon/>
      </template>

    </el-main>
  </el-container>
</template>

<script>

import { getSemesters, getDefaultSemester, updateSemester } from '../plugins/axios/apis'

export default {
  data() {
    return {
      isLoading: false,
      isSuccessful: false,
      isFailed: false,
      semester: "",
      semesterOptions: [],
    };
  },
  methods: {
    onUpdate(event) {
      event.preventDefault();
      this.isLoading = true;
      updateSemester(this.semester)
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
      this.isSuccessful = false;
      this.isFailed = false;
    },
    back() {
      window.history.back();
    },
  },
  created() {
    // assign semester to current semester
    getDefaultSemester().then((semester) => {
      this.semester = semester;
    });
    // create options for updating default
    getSemesters().then((semesters) => {
      this.semesterOptions.push(
        ...semesters.map((s) => ({ text: s.semester, value: s.semester }))
      );
    });
  },
};

</script>

<style scoped>

.description {
  font-size: 16px;
  margin-bottom: 10px;
}

.submit {
  margin-top: 12px;
}
</style>