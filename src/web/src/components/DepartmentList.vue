<template>
  <div class="d-flex flex-column flex-grow-1">
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

export default {
  name: "DepartmentList",
  components: {
  },
  props: {
    courses: Array,
    departments: Array,
  },
  computed: {
    departmentsComputed() {
      let titlelist = [];
      for(let i = 0; i < this.departments.length; i++){
        titlelist.push(this.departments[i].department);
      }
      return titlelist;
    },
  },
};
</script>

<style scoped lang="scss">
</style>
