<template>
  <div fluid class="py-3 h-100">
    <h1>Graduatation Requirements</h1>
    <b-modal ref="my-modal">
      <div class="d-block text-center" v-if="modelShowing !== null">
        <h3>{{ modelShowing }}</h3>
      </div>
    </b-modal>
    <b-row>
      <b-col sm="12">
        <p>Select your degree, graduatation year and major</p>
        <tr v-for="template in templates" :key="template.id">
          <td scope="row">{{ template.id }}</td>
        </tr>
      </b-col>
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
            {{ course.name }}
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
      this.$refs["my-modal"].show();
    },
  },
  data() {
    return {
      templates: [],
      semsterAll: [],
      modelShowing: null,
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
.draggable-placeholder-inner {
  border: 1px dashed #0088f8;
  box-sizing: border-box;
  background: rgba(0, 136, 249, 0.09);
  color: #0088f9;
  text-align: center;
  padding: 0;
  display: flex;
  align-items: center;
}
</style>
