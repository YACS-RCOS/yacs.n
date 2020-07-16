<template>
  <div class="d-flex flex-column flex-grow-1">
    <div v-for="(major, index) in majors" :key="major" role="tablist">
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
              <div id="scroll-box">
                <recycle-scroller
                  class="scroller"
                  :items="deptClassDict[major]"
                  :item-size="100"
                  typeField="vscrl_type"
                  v-slot="{ item: course }"
                >
                  <div
                    class="course-listing"
                    :class="{ 'bg-light': course.selected }"
                  >
                    <CourseListing
                      :course="course"
                      defaultAction="toggleCourse"
                      v-on="$listeners"
                      lazyLoadCollapse
                    >
                      <template #toggleCollapseButton="{ course }">
                        <button
                          v-show="
                            course.corequisites ||
                            course.prerequisites ||
                            course.raw_precoreqs
                          "
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
                  </div>
                </recycle-scroller>
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

import { RecycleScroller } from "vue-virtual-scroller";

export default {
  name: "DepartmentList",
  components: {
    CourseListing: CourseListingComponent,
    RecycleScroller,
  },
  data() {
    return {
      faInfoCircle,
    };
  },
  props: {
    majors: Array,
    deptClassDict: Object,
    selectedSemester: String,
    id: Number,
  },
};
</script>

<style scoped lang="scss">
#scroll-box {
  flex-grow: 1;
  flex-basis: 0px;
  min-height: 200px;
  border: 5px 5px solid;
}

.scroller {
  max-height: 20em;
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
