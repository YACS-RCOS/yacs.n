<template>
  <el-form
    class="form"
    ref="editSemesterForm"
    @submit.prevent="onSubmit"
  >
    <el-input
      type="hidden"
      name="semesterTitle"
      aria-label="Semester Title"
      :value="semesterTitle"
    />
    <h3>{{ semesterTitle }}</h3>
    <el-checkbox
      v-model="isPublic"
      name="isPubliclyVisible"
      style="font-variant: small-caps;"
    >
      <span v-show="isPublic">
        Public
      </span>
      <span v-show="!isPublic">
        Admin Only
      </span>
    </el-checkbox>
    <hr />
    <el-table
      :id="`edit${semesterTitle.replace(' ', '')}Tbl`"
      :data="subsemesters"
      :fields="displayedColumns"
      style="width: 100%"
    >
      <el-table-column label="Date Range">
        <template #default="scope">
          {{ formatDateRange(scope.row.date_start, scope.row.date_end) }}
        </template>
      </el-table-column>
      <el-table-column label="Semester Part Name">
        <el-input
          type="text"
          class="form-control text-dark"
          name="semester_part_name"
          label="semester_part_name"
          v-model="inputtedSemesterPartNames[subsemesters.index]"
          />
      </el-table-column>

    </el-table>
    <el-button
      @click="onSubmit"
      :class="{
        btn: true,
        'btn-primary': true,
        'my-2': true,
        'w-50': true,
        'no-cursor': isDisabled,
      }"
      @animationend="removeFeedbackClasses($event.target)"
      :disabled="isDisabled"
    >
      Update
    </el-button>
  </el-form>
</template>

<script>
import { mapDateRangeToSemesterPart as postDateMapping } from '../plugins/axios/apis'
import { standardDate } from "../utils/common.js";

export default {
  name: "EditSemesterDateNameBinding",
  props: {
    semesterTitle: String,
    semesterInfo: Object,
    subsemesters: Array,
  },
  data() {
    return {
      // eye: faEye,
      // closedEye: faEyeSlash,
      displayedColumns: ["dateRange", "semesterPartName"],
      loading: false,
      isPublic: this.semesterInfo.public,
      // My SO post. Originally, I didn't want to have to use v-model since I don't really need its full power,
      // but because of all the weirdness of the keyboard events on the semester_part input and the submit button, here I am using v-model in a v-for.
      // https://stackoverflow.com/questions/60896159/prepopulated-form-input-element-doesnt-accept-first-input-when-submit-btn-is-di/60896544#60896544
      inputtedSemesterPartNames: this.subsemesters.map(
        (item) => item.display_string
      ),
    };
  },
  methods: {
    onSubmit(event) {
      if (!this.loading) {
        console.log(this.inputtedSemesterPartNames);
        this.loading = true;
        let formData = new FormData();
        formData.append("semester_part_name", this.inputtedSemesterPartNames);
        console.log(formData);
        let submittedSemesterPartNames = formData.getAll("semester_part_name");
        console.log(submittedSemesterPartNames);
        // let submitBtn = event.target.querySelector("button[type='submit']");
        // let spinner = submitBtn.querySelector("span.spinner-border");
        // // Stop any current animation if user clicks while it's happening
        // this.removeFeedbackClasses(submitBtn);
        // this.loading = true;
        // spinner.classList.remove("d-none");
        // let formData = new FormData(event.target);
        // let submittedSemesterPartNames = formData.getAll("semester_part_name");
        postDateMapping(formData)
          .then((res) => {
            // Update the set subsemester names since the response
            // has come back with a 2xx status. Meaning we can't submit the form
            // with the same name twice (unless there's >1 input and we change one of those)
            for (var i in this.subsemesters) {
              var subsemester = this.subsemesters[i];
              subsemester.display_string = submittedSemesterPartNames[i];
            }
            // submitBtn.classList.add("success");
            console.log(res);
          })
          .catch((error) => {
            console.log(error);
            // submitBtn.classList.add("fail");
          })
          .finally(() => {
            // spinner.classList.add("d-none");
            this.loading = false;
          });
      }
    },
    removeFeedbackClasses(btn) {
      btn.classList.remove("success");
      btn.classList.remove("fail");
    },
    /***
     * @param {Date} date1
     * @param {Date} date2
     * @returns {String} date of the form "MM/DD/YYYY - MM/DD/YYYY"
     */
    formatDateRange(date1, date2) {
      return `${date1.toLocaleDateString()} - ${date2.toLocaleDateString()}`;
    },
    standardDate,
  },
  computed: {
    isDisabled() {
      // Disable if the value is falsey,
      // or if it's the same value as before
      let anyValid = false;
      for (let i = 0; i < this.inputtedSemesterPartNames.length; i++) {
        let semesterName = this.inputtedSemesterPartNames[i];
        let defaultValue = this.subsemesters[i].display_string;
        // None of the inputs can have a falsey value
        if (!semesterName) {
          return true;
        }
        let isValid = semesterName !== defaultValue;
        anyValid |= isValid;
      }
      // Disable if the visible toggle is still the same
      // TODO would like to split out this validation logic, just focusing on getting
      //      done for now
      return !(anyValid || this.isPublic !== this.semesterInfo.public);
    },
  },
};
</script>

<style scoped>
.no-cursor {
  cursor: not-allowed;
}

.form {
  text-align: center;
}

.table-title {
  text-align: center;
  color: black;
}

.el-table {
  color: "red";
  text-align: center;
}
</style>