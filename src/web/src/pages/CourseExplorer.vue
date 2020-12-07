<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="$store.state.courseList.length != 0" class="mx-auto w-75">
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
    </div>
    <CenterSpinner
      v-else
      :height="80"
      :fontSize="1.3"
      loadingMessage="Departments"
      :topSpacing="30"
    />
  </b-container>
</template>

<script>
import DepartmentListComponenet from "@/components/DepartmentList";
import { generateRequirementsText } from "@/utils";
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
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Explore",
        },
      ],
    };
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
    schoolsMajorDict() {
      let schoolsMajorDict = {};
      for (const c of this.$store.state.courseList) {
        if (!schoolsMajorDict[c.school]) {
          schoolsMajorDict[c.school] = new Set();
        }
        schoolsMajorDict[c.school].add(c.department);
      }
      return schoolsMajorDict;
    },
    deptClassDict() {
      let deptClassDict = {};
      for (const c of this.$store.state.courseList) {
        if (deptClassDict[c.department]) {
          deptClassDict[c.department].push(c);
        } else {
          deptClassDict[c.department] = [c];
        }
      }
      return deptClassDict;
    },
  },
  metaInfo() {
    return {
      title: "Explore",
      titleTemplate: "%s | YACS",
      meta: [
        { charset: 'utf-8' },
        { name: 'description', content: "Explore courses in YACS"},
        { name: 'keywords', content: "RPI, YACS, Rensselaer Polytechnic Institute"},
        { property: 'og:title', content: "RPI - YACS Course Scheduler"},
        { property: 'og:site_name', content: 'YACS'},
        { property: 'og:type', content: 'website'}
      ]
    }
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
  text-align: center;
}

.school-name {
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}
</style>
