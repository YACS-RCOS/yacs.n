<template>
  <div class="d-flex flex-column flex-grow-1">
    <div id="scroll-box">
      <div class="scroller">
        <h6
          v-for="department in departmentsComputed"
          :key="department"
          class="grid-item"
        >
          {{department}}
        </h6>
      </div>
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
#scroll-box {
  flex-grow: 1;
  flex-basis: 0px;
  min-height: 200px;
}

.scroller {
  display: grid;
  grid-template-columns: auto auto;
  height: 100%;
}
</style>
