<template id = "body">
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
          >{{ courseName }} | {{ modelShowing.creditHours }}</b-button>
        </p>
        <p
          v-if="modelShowing.Departments != null"
        >Possible categories: {{ modelShowing.Departments }}</p>
        <p
          v-if="modelShowing['pre-requsit-of'] != null"
        >Prerequsit of: {{ modelShowing["pre-requsit-of"] }}</p>
      </div>
    </b-modal>
    <b-row>
      <b-col md="6" v-for="semester in semesterAll" :key="semester['semester-name']">
        <h2>{{ semester["semester-name"] }}</h2>
        <draggable class="list-group" :list="list1" group="people">
          <b-button
            @click="showModal(course)"
            v-for="course in semester.courses"
            :key="course"
          >{{ course.name }} | {{ course.creditHours }}</b-button>
        </draggable>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { getDegreeTemplate } from "../services/YacsService";
export default {
  name: "DegreeTemplates",
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
  created() {
    getDegreeTemplate().then((list) => {
      this.templates = list;
      this.semesterAll = this.templates[0].semesters;
    });
  },
};
</script>

<style></style>
