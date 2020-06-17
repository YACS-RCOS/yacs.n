<template>
  <div class="d-flex flex-column flex-grow-1">
    <div id="scroll-box">
      <recycle-scroller
        class="scroller"
        :items="departmentsComputed"
        :item-size="40"
        typeField="vscrl_type"
        v-slot="{item: department}"
      >
        <h6>{{department}}</h6>
      </recycle-scroller>
    </div>
  </div>
</template>

<script>
import "@/typedef";

import { getDepartments } from "@/services/YacsService";

import { RecycleScroller } from "vue-virtual-scroller";

export default {
  name: "DepartmentList",
  components: {
    RecycleScroller,
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
  height: 100%;
  overflow-x: hidden;
}
</style>
