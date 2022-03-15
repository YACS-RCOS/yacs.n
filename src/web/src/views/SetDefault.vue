
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

      <el-button class="submit" type="warning" @click="onUpdate">Submit</el-button>

    </el-main>
  </el-container>
</template>

<script>

import { getSemesters, getDefaultSemester, updateSemester } from '../plugins/axios/apis'

export default {
  data() {
    return {
      loading: false,
      semester: "",
      semesterOptions: [],
    };
  },
  methods: {
    onUpdate(event) {
      event.preventDefault();
      this.loading = true;
      updateSemester(this.semester)
        .then((response) => {
          console.log(response);
          // Axios will only enter this block if the status code is 2xx,
          // so handle errors for catch block. https://stackoverflow.com/questions/49967779/axios-handling-errors

          this.loading = false;
        })
        .catch((error) => {
          console.log(error.response);
          this.loading = false;
        });
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