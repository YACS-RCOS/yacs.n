<template>
  <form
    class="my-5 text-center"
    ref="editSemesterForm"
    @submit.prevent="onSubmit"
  >
    <input
      type="hidden"
      name="semesterTitle"
      aria-label="Semester Title"
      :value="semesterTitle"
    />
    <h3>{{ semesterTitle }}</h3>
    <b-form-checkbox
      v-model="isPublic"
      name="isPubliclyVisible"
      style="font-variant: small-caps;"
    >
      <span v-show="isPublic">
        Public
        <font-awesome-icon :icon="eye" />
      </span>
      <span v-show="!isPublic">
        Admin Only
        <font-awesome-icon :icon="closedEye" />
      </span>
    </b-form-checkbox>
    <hr />
    <b-table
      :id="`edit${semesterTitle.replace(' ', '')}Tbl`"
      :items="subsemesters"
      :fields="displayedColumns"
    >
      <template v-slot:cell(dateRange)="data">
        {{ formatDateRange(data.item.date_start, data.item.date_end) }}
        <input
          type="hidden"
          name="date_start"
          label="date_start"
          :value="standardDate(data.item.date_start)"
        />
        <input
          type="hidden"
          name="date_end"
          label="date_end"
          :value="standardDate(data.item.date_end)"
        />
      </template>
      <template v-slot:cell(semesterPartName)="data">
        <input
          type="text"
          class="form-control text-dark"
          name="semester_part_name"
          label="semester_part_name"
          v-model="inputtedSemesterPartNames[data.index]"
        />
      </template>
    </b-table>
    <button
      type="submit"
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
      <b-spinner class="d-none" />
    </button>
  </form>
</template>

<script>
import { mapDateRangeToSemesterPart as postDateMapping } from "@/services/AdminService";
import { standardDate } from "@/utils";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

export default {
  name: "EditSemesterDateNameBinding",
  props: {
    semesterTitle: String,
    semesterInfo: Object,
    subsemesters: Array,
  },
  data() {
    return {
      eye: faEye,
      closedEye: faEyeSlash,
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
        let submitBtn = event.target.querySelector("button[type='submit']");
        let spinner = submitBtn.querySelector("span.spinner-border");
        // Stop any current animation if user clicks while it's happening
        this.removeFeedbackClasses(submitBtn);
        this.loading = true;
        spinner.classList.remove("d-none");
        let formData = new FormData(event.target);
        let submittedSemesterPartNames = formData.getAll("semester_part_name");
        postDateMapping(formData)
          .then((res) => {
            // Update the set subsemester names since the response
            // has come back with a 2xx status. Meaning we can't submit the form
            // with the same name twice (unless there's >1 input and we change one of those)
            for (var i in this.subsemesters) {
              var subsemester = this.subsemesters[i];
              subsemester.display_string = submittedSemesterPartNames[i];
            }
            submitBtn.classList.add("success");
            console.log(res);
          })
          .catch((error) => {
            console.log(error);
            submitBtn.classList.add("fail");
          })
          .finally(() => {
            spinner.classList.add("d-none");
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

<style lang="scss" scoped>
.no-cursor {
  cursor: not-allowed;
}
</style>
