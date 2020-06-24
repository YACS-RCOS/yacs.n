<template>
  <div class="d-flex flex-column flex-grow-1">
    <div
      v-for="(major, index) in majors"
      :index="index"
      :key="major"
      role="tablist"
    >
      <template>
        <div class="p-2 mb-1 w-100">
          <b-card-header header-tag="header" class="border-0 p-1" role="tab">
            <b-button
              block v-b-toggle="id + 'accordion-' + index"
              variant="info"
            >
              {{major}}
            </b-button>
          </b-card-header>
          <b-collapse
            :id="id + 'accordion-' + index"
            accordion="accordion"
            role="tabpanel"
          >
            <b-card-body>
              <b-card-text>TODO: Insert Major's Classes</b-card-text>
            </b-card-body>
          </b-collapse>
        </div>
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
    majors: Array,
    id: Number,
  },
  computed: {
  },
};
</script>

<style scoped lang="scss">
</style>
