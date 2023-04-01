<template id = "body">
  <div fluid class="py-3 h-100">
    <h1>Graduatation Requirements</h1>
    <b-modal ref="course-pop-up">
      <div class="d-block text-center" v-if="modelShowing != null">
        <h3>{{ modelShowing.name }}</h3>
        <p>Required credits: {{ modelShowing.creditHours }}</p>
        <p>Description: {{ modelShowing.description }}</p>
        <p v-if="modelShowing.courses != null">
          <b-button
            @click="changeTitle(courseName)"
            v-for="courseName in modelShowing.courses"
            :key="courseName"
          >{{ courseName }} | {{ modelShowing.creditHours }}</b-button>
        </p>
        <p
          v-if="modelShowing.Departments != null"
        >Possible categories: {{ modelShowing.Departments }}</p>
        <p
          v-if="modelShowing['pre-requsit-of'] != null"
        >Prerequsite of: {{ modelShowing["pre-requsite-of"] }}</p>
      </div>
    </b-modal>
    <b-row>
      <b-col sm="4">
        <b-form-select v-model="selected" :options="optionsDegree"></b-form-select>
      </b-col>
      <b-col sm="4">
        <b-form-select v-model="selected" :options="optionsMajor"></b-form-select>
      </b-col>
      <b-col sm="4">
        <b-form-select v-model="selected" :options="optionsYear"></b-form-select>
      </b-col>
      <tr v-for="template in templates" :key="template.Major" text-align:center>
        <td scope="row">{{ template.id }}</td>
      </tr>
    </b-row>
    <b-row>
      <b-col md="6" v-for="semester in semesterAll" :key="semester['semester-name']">
        <h2>{{ semester["semester-name"] }}</h2>
        <draggable class="list-group" :list="list1" group="people">
          <b-button
            @click="displayCourse(course)"
            v-for="course in semester.courses"
            :key="course"
          >{{ course.name }} | {{ course.creditHours }}</b-button>
        </draggable>
      </b-col>
    </b-row>
  </div>
</template>


<script>
// import { getDegreeTemplate } from "../services/YacsService";
import  draggable  from "vuedraggable";
import  degree_json from "./DegreeTemplatesFormatted.json";
//import DepartmentListComponenet from "@/components/DepartmentList";
export default {
  name: "DegreeTemplates",
  components: {
    draggable,
    //DepartmentList: DepartmentListComponenet,
  },
  methods: {
    displayCourse(course) {
      this.courseInfo = course;
      this.courseInfo.subName = null;
      this.$refs["course-pop-up"].show();
    },
    changeTitle(courseName) {
      this.courseInfo.name = courseName;
    },
  },
  data() {
    return {
      templates: [],
      semsterAll: [],
      courseInfo: null,
      degree: "UNGD",
      selected: null,
      /* below if for the dropdown boxes */
      optionsDegree: [
        { text: "Plese select a Degree" },
        { text: "GRAD" },
        { text: "UNGD" },
      ],
      optionsYear: [
        { text: "Plese select your entering Year" },
        { text: "2019" },
        { text: "2020" },
        { text: "2021" },
        { text: "2022" },
      ],
      optionsMajor: [
        { text: "Plese select your major" },
      ],
    };
  },

  created() {
    this.templates = degree_json;
    for (var i = 0; i < this.templates.length; i++){
      this.optionsMajor.push({text: degree_json[i]["Major"]});
      console.log(this.templates[i]["Major"]);
    }
    // getDegreeTemplate().then((list) => {
    //   this.templates = list;
    //   this.semesterAll = this.templates[0].semesters;
    // });
  },
};
</script>

<style>
body {
  text-align: center;
}
.draggable-placeholder-inner {
  border: 1px dashed #0088f8;
  box-sizing: border-box;
  background: red;
  color: red;
  text-align: center;
  padding: 10px;
  display: flex;
  align-items: center;
}
</style>
