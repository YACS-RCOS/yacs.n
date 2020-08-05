<template>
  <div v-if="ready" class="gridContainer w-100 mb-4">
    <b-row>
      <b-col>
        <b-row v-for="n in 3" :key="n" class="departmentBox border m-2 mb-4">
          <b-col>
            <b-row class="school-name">
              <h2 class="m-2 ml-3">School Name (i.e. HASS)</h2>
            </b-row>
            <b-row>
              <DepartmentList
                :majors="coursesChunked[n - 1]"
                :id="n"
              ></DepartmentList>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
      <b-col>
        <b-row v-for="n in 3" :key="n" class="departmentBox border m-2 mb-4">
          <b-col>
            <b-row class="school-name">
              <h2 class="m-2 ml-3">School Name (i.e. HASS)</h2>
            </b-row>
            <b-row>
              <DepartmentList
                :majors="coursesChunked[n + 2]"
                :id="n + 3"
              ></DepartmentList>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </div>
  <div v-else>
    <b-spinner></b-spinner>
    <strong class="m-2">Loading courses...</strong>
  </div>
</template>

<script>
import { getCourses } from "../services/YacsService";
import DepartmentListComponenet from "@/components/DepartmentList";

export default {
  name: "CourseExplorer",
  components: {
    DepartmentList: DepartmentListComponenet,
  },
  props: {
    selectedSemester: String,
  },
  data() {
    return {
      //an object with keys being the dept, and values a list of courses
      deptClassDict: {},
      ready: false,
    };
  },
  async created() {
    getCourses(this.selectedSemester).then((courses) => {
      for (const c of courses) {
        if (this.deptClassDict[c.department]) {
          this.deptClassDict[c.department].push(c);
        } else {
          this.deptClassDict[c.department] = [c];
        }
      }
      this.ready = true;
    });
  },
  computed: {
    coursesChunked() {
      const arr = Object.keys(this.deptClassDict);
      const chunkedArr = [];
      const noOfChunks = Math.ceil(arr.length / 6);
      for (var i = 0; i < noOfChunks; i++) {
        chunkedArr.push(arr.slice(i * 6, (i + 1) * 6));
      }
      return chunkedArr;
    },
  },
};
</script>

<style>
.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}

.departmentBox {
  width: 30rem;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
}

.school-name {
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}
</style>
