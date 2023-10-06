<template>
  <b-container class="mt-3">
    <section id="MapDateRangeToName">
      <h2>Assign Semester Part Name to Date Ranges</h2>
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
              (sem_info) => sem_info.semester === standardSemesterName,
            )
          "
        />
      </div>
    </section>
  </b-container>
</template>

<script>
import { getSubSemesters } from "@/services/YacsService";
import { getAllSemesterInfo } from "@/services/AdminService";
import EditSemesterDateNameBinding from "@/components/EditSemesterDateNameBinding.vue";

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
    getSubSemesters().then((subsemesters) => {
      this.subsemesters = subsemesters;
      this.standardSemesterNames = new Set(
        subsemesters.map((subsemester) => subsemester.semester_name),
      );
    });
    getAllSemesterInfo().then((sem_infos) => {
      this.semesterInfos = sem_infos;
    });
  },
};
</script>

<style lang="scss">
$danger: #dc3545;
$success: #28a745;
$primary: #007bff;

.success {
  animation: success ease-in-out 2s;
}

.fail {
  animation: fail ease-in-out 2s;
}

@keyframes success {
  50% {
    background-color: $success;
  }
  to {
    background-color: $primary;
  }
}

@keyframes fail {
  50% {
    background-color: $danger;
  }
  to {
    background-color: $primary;
  }
}
</style>
