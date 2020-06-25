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
          <b-button
            squared
            v-b-toggle="id + 'accordion-' + index"
            variant="light"
            class="major-button m-0 ml-2"
          >
            {{ major }}
          </b-button>
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
  components: {},
  props: {
    majors: Array,
    id: Number,
  },
  computed: {},
};
</script>

<style scoped lang="scss">
.major-button {
  display: inline;
  background: white;
  border-style: none;
  text-align: justify;
  width: 95%;
}

.major-button:hover {
  //important because when you click the color changes and thats annoying
  background: rgba(108, 90, 90, 0.15) !important;
}
</style>
