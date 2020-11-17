import "@/typedef";

// eslint-disable-next-line no-unused-vars
import { VueCookies } from "vue-cookies";

const COOKIE_KEY = "selectedCourses";

class SelectedCoursesCookie {
  /**
   * @typedef SelectedCourse
   * @property {string} id
   * @property {string[]} selectedSectionCrns
   *
   * @typedef SelectedSemesters
   * @type {{[semester: string]: SelectedCourse[]}}
   */

  /**
   * @param {VueCookies} $cookies
   * @param {SelectedCourse[]} selectedCourses
   * @private
   */
  constructor($cookies, selectedSemesters) {
    /**
     * @type {VueCookies}
     * @private
     */
    this.$cookies = $cookies;
    /**
     * @type {SelectedSemesters}
     * @private
     */
    this.selectedSemesters = selectedSemesters;
  }

  /**
   *
   * @param {VueCookies} $cookies
   * @returns {null|SelectedCoursesCookie}
   */
  static load($cookies) {
    return new SelectedCoursesCookie(
      $cookies,
      $cookies.isKey(COOKIE_KEY) ? $cookies.get(COOKIE_KEY) : {}
    );
  }

  save() {
    this.$cookies.set(COOKIE_KEY, this.selectedSemesters);
    console.log(JSON.stringify(this.selectedSemesters, undefined, 2));
  }

  /**
   *
   * @param {string} semester
   * @returns {SelectedCourse[]}
   */
  getSelectedCourses(semester) {
    if (this.selectedSemesters[semester] === undefined) {
      this.selectedSemesters[semester] = [];
    }

    return this.selectedSemesters[semester];
  }

  /**
   * @param {string} semester
   * @param {string} id
   * @returns {Course}
   */
  getSelectedCourse(semester, id) {
    const selectedCourses = this.getSelectedCourses(semester);

    const selectedCourse = selectedCourses.find(
      (selectedCourse) => selectedCourse.id === id
    );

    if (selectedCourse === undefined) {
      const newSelectedCourse = { id, selectedSectionCrns: [] };

      selectedCourses.push(newSelectedCourse);

      return newSelectedCourse;
    } else {
      return selectedCourse;
    }
  }

  /**
   * Only adds an entry for the course, to add sections, call `addCourseSection`
   * @param {string} semester
   * @param {Course} course
   */
  addCourse(semester, course) {
    this.getSelectedCourse(semester, course.id);

    return this;
  }

  /**
   * @param {string} semester
   * @param {Course} course
   * @param {CourseSection} section
   */
  addCourseSection(semester, course, section) {
    this.getSelectedCourse(semester, course.id).selectedSectionCrns.push(
      section.crn
    );
    return this;
  }

  /**
   * @param {string} semester
   * @param {Course} course
   */
  removeCourse(semester, course) {
    this.selectedSemesters[semester] = this.getSelectedCourses(semester).filter(
      (selectedCourse) => selectedCourse.id !== course.id
    );

    return this;
  }

  /**
   *
   * @param {string} semester
   * @param {CourseSection} section
   */
  removeCourseSection(semester, section) {
    const selectedCourse = this.getSelectedCourses(
      semester
    ).find((selectedCourse) =>
      selectedCourse.selectedSectionCrns.some((crn) => crn === section.crn)
    );

    selectedCourse.selectedSectionCrns = selectedCourse.selectedSectionCrns.filter(
      (crn) => crn !== section.crn
    );

    return this;
  }
}

export { SelectedCoursesCookie };
