<template id="body">
  <div fluid class="py-3 h-100">
    <h1>Graduatation Requirements</h1>
    <b-modal ref="my-modal">
      <div class="d-block text-center" v-if="modelShowing != null">
        <h3>{{ modelShowing.name }}</h3>
        <p>Required credits: {{ modelShowing.creditHours }}</p>
        <p>Description: {{ modelShowing.description }}</p>
        <p v-if="modelShowing.courses != null">
          <b-button
            @click="changeTitle(courseName)"
            v-for="courseName in modelShowing.courses"
            :key="courseName"
          >
            {{ courseName }} | {{ modelShowing.creditHours }}
          </b-button>
        </p>
        <p v-if="modelShowing.Departments != null">
          Possible categories: {{ modelShowing.Departments }}
        </p>
        <p v-if="modelShowing['pre-requsit-of'] != null">
          Prerequsit of: {{ modelShowing["pre-requsit-of"] }}
        </p>
      </div>
    </b-modal>
    <b-row>
      <b-col sm="4">
        <b-form-select
          v-model="selected"
          :options="optionsDegree"
        ></b-form-select>
      </b-col>
      <b-col sm="4">
        <b-form-select
          v-model="selected"
          :options="optionsMajor"
        ></b-form-select>
      </b-col>
      <b-col sm="4">
        <b-form-select
          v-model="selected"
          :options="optionsYear"
        ></b-form-select>
      </b-col>
      <tr v-for="template in templates" :key="template.id" text-align:center>
        <td scope="row">{{ template.id }}</td>
      </tr>
    </b-row>
    <b-row>
      <b-col
        md="6"
        v-for="semester in semesterAll"
        :key="semester['semester-name']"
      >
        <h2>{{ semester["semester-name"] }}</h2>
        <draggable class="list-group" :list="list1" group="people">
          <b-button
            @click="showModal(course)"
            v-for="course in semester.courses"
            :key="course"
          >
            {{ course.name }} | {{ course.creditHours }}
          </b-button>
        </draggable>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { getDegreeTemplate } from "../services/YacsService";
//import DepartmentListComponenet from "@/components/DepartmentList";
import draggable from "vuedraggable";
export default {
  name: "DegreeTemplates",
  components: {
    draggable,
    //DepartmentList: DepartmentListComponenet,
  },
  methods: {
    showModal(course) {
      this.modelShowing = course;
      this.modelShowing.subName = null;
      this.$refs["my-modal"].show();
    },
    changeTitle(courseName) {
      this.modelShowing.name = courseName;
    },
  },
  data() {
    return {
      templates: [],
      semsterAll: [],
      modelShowing: null,
      degree: "UNGD",
      selected: null,
      optionsDegree: [
        { text: "Plese select a Degree" },
        { text: "GRAD" },
        { text: "UNGD" },
      ],
      optionsYear: [
        { text: "Plese select your entering Year" },
        { text: "2017" },
        { text: "2018" },
        { text: "2019" },
        { text: "2020" },
      ],
      optionsMajor: [
        { text: "Plese select your major" },
        { text: "CSCI" },
        { text: "ITWS" },
      ],
    };
  },

  created() {
    getDegreeTemplate().then((list) => {
      this.templates = list;
      this.semesterAll = this.templates[0].semesters;
    });
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
