<template>
  <div v-if="ready" class="gridContainer w-100">
    <b-row>
      <b-col>
        <b-row
          v-for="n in 3"
          :key="n"
          class="departmentBox border m-2"
        >
          <b-col>
            <b-row>
              <h2>School Name (i.e. HASS)</h2>
            </b-row>
            <b-row>
              <DepartmentList :majors="coursesChunked[n-1]" :id="n"></DepartmentList>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
      <b-col>
        <b-row
          v-for="n in 3"
          :key="n"
          class="departmentBox border m-2"
        >
          <b-col>
            <b-row>
              <h2>School Name (i.e. HASS)</h2>
            </b-row>
            <b-row>
              <DepartmentList :majors="coursesChunked[n+2]" :id="n+2"></DepartmentList>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
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
      for(let c of courses){
        if(this.deptClassDict[c.department]){
          this.deptClassDict[c.department].push(c);
        }else{
          this.deptClassDict[c.department] = [c];
        }
      }
      this.ready = true;
    });
  },
  computed: {
    coursesChunked() {
      let arr = Object.keys(this.deptClassDict);
      let chunkedArr = [];
      let noOfChunks = Math.ceil(arr.length/6);
      for(var i=0; i<noOfChunks; i++){
        chunkedArr.push(arr.slice(i*6, (i+1)*6));
      }
      return chunkedArr;
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
  width: 30rem;
  box-shadow: 5px 5px #888888;
  text-align: center;
}
</style>
