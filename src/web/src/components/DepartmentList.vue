<template>
  <div class="d-flex flex-column flex-grow-1">
    <!-- LOOP Through the majors list -->
    <div v-for="(major, index) in majors" :key="major" role="tablist">
      <template>
        <div class="mt-1 mb-1 w-100">
          <!-- Subject button -->
          <b-button
            squared
            v-b-toggle="id + 'accordion-' + index"
            variant="light"
            class="major-button m-0 ml-1"
            :to="{
              name: 'SubjectExplorer',
              params: { subject: major },
            }"
          >
            <b class="majorShort">{{ major }}</b>
            - {{ getLongName(major) }}
          </b-button>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import "@/typedef";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { getLongName } from "@/utils";

export default {
  name: "DepartmentList",
  components: {},
  data() {
    return {
      faInfoCircle,
    };
  },
  props: {
    majors: Set,
    deptClassDict: Object,
    id: Number,
  },

  /**
   * courseInfoModalToggle
   * Display the course object information onn console
   */
  methods: {
    getLongName,
    courseInfoModalToggle(course) {
      console.log(course);
    },
  },
};
</script>

<style scoped lang="scss">
.major-button {
  display: inline-block;
  background: white;
  border-style: none;
  text-align: justify;
  width: 95%;
}

.major-button:hover {
  //important because when you click the color changes and thats annoying
  background: rgba(108, 90, 90, 0.15) !important;
}

.majorShort {
  color: #3395ff;
}

</style>
