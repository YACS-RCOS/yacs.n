<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

    <!-- button to switch between alphabet order and department order -->
    <div style="float: left;" class="w-10">
      <b-button 
        class="button"
        @click="listAlphabet()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >
        List by Alphabet
      </b-button>
      <br />
      <b-button
        class="button"
        @click="listDept()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >
        List by Department
      </b-button>
    </div>

    <div v-if="!isLoadingCourses && courses.length > 0" class="mx-auto w-75">
      <b-row>
        <!-- 2 arrays in schoolDepartmentObjects, so 2 columns -->
        <b-col
          v-for="(deptCol, index) in schoolDepartmentObjects"
          :key="`deptCol-${index}`"
          md="6"
          v-show="cateShow"
        >
          <b-row
            v-for="deptObj in deptCol"
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
                  v-on:showCourseInfo="showCourseInfo($event)"
                ></DepartmentList>
              </b-row>
            </b-col>
          </b-row>
        </b-col>

        <!-- splitted Departments in alphabet order -->
        <b-col
          v-for="(deptCol, index) in alphDepartmentObjects"
          :key="`deptCol-${index}`"
          md="6"
          v-show="alphShow"
        >
          <b-row
            v-for="deptObj in deptCol"
            :key="deptObj.letter"
            class="departmentBox border m-2 mb-4"
          >
            <b-col>
              <!-- Alphabet Title  -->
              <b-row class="school-name">
                <h3 class="m-1 ml-2">
                  {{ deptObj.letter }}
                </h3>
              </b-row>
              <!-- Subject Title  -->
              <b-row>
                <DepartmentList
                  :majors="deptObj.departments"
                  :deptClassDict="deptClassDict"
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
import { mapGetters, mapState } from "vuex";
import { COURSES } from "@/store";
import DepartmentListComponenet from "@/components/DepartmentList";
import { generateRequirementsText } from "@/utils";
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  name: "CourseExplorer",
  components: {
    DepartmentList: DepartmentListComponenet,
    CenterSpinner: CenterSpinnerComponent,
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
      cateShow: true,
      alphShow: false,
    };
  },
  methods: {
    listAlphabet() {
      this.cateShow = false;
      this.alphShow = true;
    },
    listDept() {
      this.cateShow = true;
      this.alphShow = false;
    },
    generateRequirementsText,
  },
  computed: {
    ...mapState(["isLoadingCourses"]),
    ...mapGetters([COURSES]),
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

    // similar to schoolDepartmentObjects() but creating two columns
    // of departments separated by alphabetical letters 
    alphDepartmentObjects() {
      let keyArr = Object.entries(this.alphDeptDict)
        .map((alphDepartmentMapping) => ({
          letter: alphDepartmentMapping[0],
          departments: alphDepartmentMapping[1],
        }))
      let columnArr = [[], []];
      // separates into two columns based on number of letters
      for (let i = 0; i < keyArr.length; i++) {
        if (i < keyArr.length / 2) {
          columnArr[0].push(keyArr[i]);
        } else {
          columnArr[1].push(keyArr[i]);
        }
      }
      return columnArr;
    },

    schoolsMajorDict() {
      let schoolsMajorDict = {};
      for (const c of this.courses) {
        if (!schoolsMajorDict[c.school]) {
          schoolsMajorDict[c.school] = new Set();
        }
        schoolsMajorDict[c.school].add(c.department);
      }
      return schoolsMajorDict;
    },

    deptClassDict() {
      let deptClassDict = {};
      for (const c of this.courses) {
        if (deptClassDict[c.department]) {
          deptClassDict[c.department].push(c);
        } else {
          deptClassDict[c.department] = [c];
        }
      }
      return deptClassDict;
    },

    // similar to schoolsMajorDict() and deptClassDict()
    // map/set with a set of departments for each alphabetical letter
    alphDeptDict(){
      let alphDeptDict = {};
      for (const c of this.courses){
        if (!alphDeptDict[c.department[0]]){
          alphDeptDict[c.department[0]] = new Set();
        }
        alphDeptDict[c.department[0]].add(c.department);
      }
      return alphDeptDict;
    },
  },
  metaInfo() {
    return {
      title: "Explore",
      titleTemplate: "%s | YACS",
      meta: [
        { charset: "utf-8" },
        {
          vmid: "description",
          name: "description",
          content: "Explore courses in YACS",
        },
        {
          name: "keywords",
          content: "RPI, YACS, Rensselaer Polytechnic Institute",
        },
        { property: "og:title", content: "RPI - YACS Course Scheduler" },
        { property: "og:site_name", content: "YACS" },
        { property: "og:type", content: "website" },
      ],
    };
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
  color: #3395ff;
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}

.button:hover {
  background: rgba(108, 90, 90, 0.15) !important;
}

</style>
