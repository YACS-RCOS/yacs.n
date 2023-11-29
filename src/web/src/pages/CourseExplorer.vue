<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="!isLoadingCourses && courses.length > 0" class="mx-auto w-75">
      <b-row>
        <b-col
          v-for="(deptCol, index) in schoolDepartmentObjects"
          :key="`deptCol-${index}`"
          cols="12"
        >
          <b-row
            v-for="deptObj in deptCol"
            :key="deptObj.school"
            class="departmentBox m-2 mb-4"
          >
            <b-col cols="12">
            <!-- Department Title as a ~button that controls the collapse -->
              <b-button
                v-b-toggle="'collapse-' + deptObj.school"
                class="button"
                variant="outline-secondary"
              >
                <h4>
                  {{ deptObj.school }}
                  <span class="chevron"></span>
                </h4>
              </b-button>          
              <hr />
              <!-- Subject Title inside a b-collapse -->
              <b-collapse :id="'collapse-' + deptObj.school">
                <b-row>
                  <DepartmentList
                    :majors="deptObj.departments"
                    :deptClassDict="deptClassDict"
                    v-on:showCourseInfo="showCourseInfo($event)"
                  ></DepartmentList>
                </b-row>
              </b-collapse>
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
    };
  },
  methods: {
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

.button {
  width: 100%;
  text-align: left;
  background-color: transparent;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 0;
  margin: 0;
  font-size: 2rem;
  font-weight: 500;
  color: #3395ff !important;
  text-decoration: none;
  transition: background-color 0.3s, color 0.3s;
}

.button:hover {
  background-color: rgba(108, 90, 90, 0.15);
}

.button:focus {
  background-color: transparent;
  box-shadow: none !important;
  outline: none !important;

}

.button:active {
  background-color: transparent !important;
  color: #3395ff;
  box-shadow: none !important;
  outline: none !important;
}

.chevron {
  display: inline-block;
  width: 0;
  height: 0;
  margin-left: auto;
  border-style: solid;
  border-width: 0 5px 10px;
  border-color: transparent transparent #3395ff;
  transition: transform 0.3s;
}

/* Rotate the chevron when the button is active */
.button[aria-expanded="true"] .chevron {
  transform: rotate(180deg);
  margin-left: auto;
}

</style>
