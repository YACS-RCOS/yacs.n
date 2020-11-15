<template>
  <b-container v-if="ready">
    <b-row>
      <!--
        - Left side of the column
      -->
      <b-col>
        <b-row
          v-for="deptObj in schoolDepartmentObjects[0]"
          :key="deptObj.school"
          class="departmentBox border m-2 mb-4"
        >
          <b-col>
            <!-- Department Title  -->
            <b-row class="school-name">
              <h3 class="m-1 ml-2">
                {{ deptObj.school }}
              </h3>
            </b-row>
            <!-- Subject Title  -->
            <b-row>
              <DepartmentList
                :majors="deptObj.departments"
                :deptClassDict="deptClassDict"
                :selectedSemester="selectedSemester"
                v-on:showCourseInfo="showCourseInfo($event)"
              ></DepartmentList>
            </b-row>
          </b-col>
        </b-row>
      </b-col>

      <!-- Right side of the column  -->
      <b-col>
        <b-row
          v-for="deptObj in schoolDepartmentObjects[1]"
          :key="deptObj.school"
          class="departmentBox border m-2 mb-4"
        >
          <b-col>
            <b-row class="school-name">
              <h3 class="m-1 ml-2">
                {{ deptObj.school }}
              </h3>
            </b-row>
            <b-row>
              <DepartmentList
                :majors="deptObj.departments"
                :deptClassDict="deptClassDict"
                :selectedSemester="selectedSemester"
                v-on:showCourseInfo="showCourseInfo($event)"
              ></DepartmentList>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
  <div id="spinnerWrapper" v-else>
    <CenterSpinner
      :height = "80"
      :fontSize = "1.3"
      loadingMessage = "Departments"
      :topSpacing = "30"
    />
  </div>
</template>

<script>
import { getCourses } from "../services/YacsService";
import DepartmentListComponenet from "@/components/DepartmentList";
import { generateRequirementsText } from "@/utils";
import { getDefaultSemester } from "@/services/AdminService";
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  name: "CourseExplorer",
  components: {
    DepartmentList: DepartmentListComponenet,
    CenterSpinner: CenterSpinnerComponent,
  },
  props: {
    selectedSemester: String,
  },
  data() {
    return {
      //an object with keys being the dept, and values a list of courses
      deptClassDict: {},
      schoolsMajorDict: {},
      ready: false,
    };
  },
  async created() {
    if (this.selectedSemester === "") {
      const querySemester = this.$route.query.semester;
      this.selectedSemester =
        querySemester && querySemester !== "null"
          ? querySemester
          : await getDefaultSemester();
    }
    getCourses(this.selectedSemester).then((courses) => {
      for (const c of courses) {
        if (!this.schoolsMajorDict[c.school]) {
          this.schoolsMajorDict[c.school] = new Set();
        }
        this.schoolsMajorDict[c.school].add(c.department);
        if (this.deptClassDict[c.department]) {
          this.deptClassDict[c.department].push(c);
        } else {
          this.deptClassDict[c.department] = [c];
        }
      }
      this.ready = true;
    });
  },
  methods: {
    generateRequirementsText,
  },
  computed: {
    schoolDepartmentObjects() {
      let keyArr = Object.entries(this.schoolsMajorDict)
        .map((schoolDepartmentMapping) => ({
          school: schoolDepartmentMapping[0],
          departments: schoolDepartmentMapping[1],
        }))
        .sort((left, right) => right.departments.size - left.departments.size);
      let columnArr = [[], []];
      //This is a greedy alg for solving the partition problem
      for (let i = 0; i < keyArr.length; i++) {
        if (i % 2 === 0) {
          columnArr[0].push(keyArr[i]);
        } else {
          columnArr[1].push(keyArr[i]);
        }
      }
      return columnArr;
    },
  },
};
</script>

<style>
.departmentBox {
  text-align: center;
}

.school-name {
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}
</style>
