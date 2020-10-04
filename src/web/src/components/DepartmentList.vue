<template>
  <div class="d-flex flex-column flex-grow-1">
    <div v-for="(major, index) in majors" :key="major" role="tablist">
      <template>
        <div class="mt-1 mb-1 w-100">
          <b-button
            squared
            v-b-toggle="id + 'accordion-' + index"
            variant="light"
            class="major-button m-0 ml-1"
          >
            {{ major }}
          </b-button>
          <b-collapse
            :id="id + 'accordion-' + index"
            accordion="accordion"
            role="tabpanel"
          >
            <b-card-body>
              <div id="scroll-box">
                <ul class="scroller">
                  <li
                    class="course-listing"
                    v-for="course in deptClassDict[major]"
                    :key="course.name + course.date_start + course.date_end"
                    :class="{ 'bg-light': course.selected }"
                  >
                    <router-link
                      :to="{
                        name: 'CoursePage',
                        params: { course: course.name },
                      }"
                    >
                      {{ course.name }}
                    </router-link>
                    <CourseListing
                      :course="course"
                      :showAddButton="false"
                      defaultAction="showInfoModal"
                      v-on="$listeners"
                      lazyLoadCollapse
                    >
                      <template #toggleCollapseButton="{ course }">
                        <button
                          v-show="false"
                          class="btn"
                          @click.stop="courseInfoModalToggle(course)"
                        >
                          <font-awesome-icon :icon="faInfoCircle" />
                        </button>
                      </template>
                      <template #collapseContent>
                        {{ null }}
                      </template>
                    </CourseListing>
                  </li>
                </ul>
              </div>
            </b-card-body>
          </b-collapse>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import "@/typedef";
import CourseListingComponent from "@/components/CourseListing";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";

export default {
  name: "DepartmentList",
  components: {
    CourseListing: CourseListingComponent,
  },
  data() {
    return {
      faInfoCircle,
    };
  },
  props: {
    majors: Set,
    deptClassDict: Object,
    selectedSemester: String,
    id: Number,
  },
  methods: {
    courseInfoModalToggle(course) {
      console.log(course);
    },
  },
};
</script>

<style scoped lang="scss">
#scroll-box {
  flex-grow: 1;
  flex-basis: 0px;
  min-height: 200px;
  border: 1px rgba(108, 90, 90, 0.15) solid;
  padding: 0 1em 0 1em;
}

.scroller {
  max-height: 20em;
  overflow-x: hidden;
  text-align: left;
  list-style: none;
  padding-left: 0;
}

.course-listing {
  height: 100px;
  padding-top: 10px;
  border-top: 1px solid #e9ecef;
  border-bottom: 1px solid #e9ecef;
}

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
