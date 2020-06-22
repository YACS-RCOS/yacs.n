<template>
  <div class="d-flex flex-column flex-grow-1">
    <!-- <div id="scroll-box">
      <div class="border-left border-top scroller">
        <b-collapse
          accordion= "accordion"
          v-for="department in departmentsComputed"
          :key="department"
          class="border-right border-bottom grid-item"
        >
          <h6 class="p-0 m-0">{{department}}</h6>
        </b-collapse>
      </div>
    </div> -->
    <div
      v-for="(department, index) in departmentsComputed"
      :index="index"
      :key="department"
      role="tablist"
    >
      <template>
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle="'accordion-' + index" variant="info">{{department}}</b-button>
          </b-card-header>
          <b-collapse :id="'accordion-' + index" accordion="accordion" role="tabpanel">
            <b-card-body>
              <b-card-text>This is some tester text</b-card-text>
            </b-card-body>
          </b-collapse>
        </b-card>
      </template>
    </div>
  </div>
</template>

<script>
import "@/typedef";

import { getDepartments } from "@/services/YacsService";

export default {
  name: "DepartmentList",
  components: {
  },
  props: {
    courses: Array,
  },
  data() {
    return {
      departments: [],
    };
  },
  created() {
    getDepartments().then((departments) => {
      this.departments=departments;
      console.log(this.departments[0]);
    });
  },
  computed: {
    departmentsComputed() {
      let titlelist = [];
      for(var i = 0; i < this.departments.length; i++){
        titlelist.push(this.departments[i].department);
      }
      return titlelist;
    },
  },
};
</script>

<style scoped lang="scss">
</style>
