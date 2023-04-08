<template id = "body">
  <div fluid class="py-3 h-100">
    <h1>Degree Requirement Tempaltes</h1>
    
    <!-- This is a popup that appears when a course is clicked -->
    <b-modal ref="course-pop-up">
      <!-- Course Info for each course
       <div class="d-block text-center" v-if="courseData != null">
        <h3>{{ courseData.name }}</h3>
        <p>Required credits: {{ courseData.creditHours }}</p>
        <p>Description: {{ courseData.description }}</p>
        <p v-if="courseData.courses != null">
          <b-button
            @click="changeTitle(courseName)"
            v-for="courseName in courseData.courses"
            :key="courseName"
          >{{ courseName }} | {{ courseData.creditHours }}</b-button>
        </p>
        <p
          v-if="courseData.Departments != null"
        >Possible categories: {{ courseData.Departments }}</p>
        <p
          v-if="courseData['pre-requsite-of'] != null"
        >Prerequsite of: {{ courseData["pre-requsite-of"] }}</p>
      </div> -->
    </b-modal>




    <b-row sm = "3" justify = "center" align-h = "center" gutter ="sm">
      <!-- <b-col sm="4">
        <b-form-select v-model="selected" :options="optionsDegree"></b-form-select>
      </b-col> -->
      <b-col sm="4">
        <b-form-select v-model="selected" :options="optionsMajor"></b-form-select>
      </b-col>
      <b-col sm="4">
        <b-form-select v-model="selected" :options="optionsYear"></b-form-select>
      </b-col>
      <tr v-for="template in templates" :key="template.Major" text-align:center>
        <td scope="row">{{ template.Major }}</td>
      </tr>
    </b-row>
    <b-row>
      <b-col md="6" v-for="semester in semesterAll[selected]" :key="semester['semester_name']">
        <h2>{{ semester["semester_name"] }}</h2>
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
      this.courseData = course;
      this.courseData.subName = null;
      this.$refs["course-pop-up"].show();
    },
    changeTitle(courseName) {
      this.courseData.name = courseName;
    },
  },
  data() {
    return {
      templates: [],
      semsterAll: {},
      courseData: {},
      degree: "UNGD",
      selected: null,
      /* below if for the dropdown boxes prob don't need an undergrad option but
         we could add a minors/majors option eventually
      */
      // optionsDegree: [
      //   { text: "Plese select a Degree" },
      //   { text: "GRAD" },
      //   { text: "UNGD" },
      // ],
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
    for (let i = 0; i < this.templates.length; i++){
      this.optionsMajor.push({text: degree_json[i].Major});
    }

    let semesterMap = {
      Y1S1: "Semester One",
      Y1S2: "Semester Two",
      Y2S1: "Semester Three",
      Y2S2: "Semester Four",
      Y3S1: "Semester Five",
      Y3S2: "Semester Six",
      Y4S1: "Semester Seven",
      Y4S2: "Semester Eight"
    }


    for (const major in this.templates){
      for(const key in major){
        
        //check if the item is a description of a semester 
        if(key.length == 4 && key[0] == 'Y' && key[2] == 'S'){
          
          // current semester in the json file
          let semester = major[key];

          // creates a new dictionary to print the semesters in the format Semester # (Season/Arch)
          this.semesterAll[major][semesterMap[key]] = {
              semeseter_name: semesterMap[key].concat('(', semester[0], ')'),
              courses_and_credits: []
          };

          // iterate through courses in a semester of a major and parse the course string
          let temp_course_list = []
          for(let i = 1; i < semester.length; i++){
            let description = semester[i];
            let regex = /Course: | CreditHours: /;
            let split_description = description.split(regex);
            if(split_description.length != 2) continue;
            temp_course_list.push([split_description[0], split_description[1]]);
          }

          this.semesterAll[major][semesterMap[key]].courses_and_credits = temp_course_list;
        }
      }
    }


    /*
     * find some way to get the course data for a specific course
     *    This will probably help with learning the database
     * create a datastructure to pair these courses, course data, and majors together
     * add the data to the formatting of the preexisting page
     */

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
