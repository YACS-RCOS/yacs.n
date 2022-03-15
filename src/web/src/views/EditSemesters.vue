
<template>
  <el-container>
    <el-main>
      <div class="description">
        Assign Semetser Part Name to Date Ranges
      </div>

      <!-- Can't put v-if in conjunction with v-for, so using div wrapper -->
      <div v-if="semesterInfos.length">
        <EditSemester
          v-for="(standardSemesterName, key) in standardSemesterNames"
          :key="key"
          :semesterTitle="standardSemesterName"
          :subsemesters="
            subsemesters.filter((x) => x.semester_name === standardSemesterName)
          "
          :semesterInfo="
            semesterInfos.find(
              (sem_info) => sem_info.semester === standardSemesterName
            )
          "
        />
      </div>

    </el-main>
  </el-container>
</template>

<script>
import { getSubsemesters } from '../plugins/axios/apis';
import { getAllSemesterInfo } from '../plugins/axios/apis';
import EditSemesterDateNameBinding from "../components/EditSemesterDateNameBinding.vue";

export default {
  name: "EditSemesters",
  props: {},
  components: {
    EditSemester: EditSemesterDateNameBinding,
  },
  data() {
    return {
      subsemesters: [],
      semesterInfos: [],
      standardSemesterNames: [],
    };
  },
  created() {
    getSubsemesters().then((subsemesters) => {
      this.subsemesters = subsemesters;
      this.standardSemesterNames = new Set(
        subsemesters.map((subsemester) => subsemester.semester_name)
      );
    });
    getAllSemesterInfo().then((sem_infos) => {
      this.semesterInfos = sem_infos;
      console.log("triggered")
    });
  },
};
</script>

<style scoped>

.description {
  font-size: 16px;
  margin-bottom: 10px;
}

</style>