import "@/typedef";

// eslint-disable-next-line no-unused-vars
import { VueCookies } from "vue-cookies";

const COOKIE_KEY = "finalExams";

/**
 * Handy module for managing selected courses cookie storage
 *
 * @example
 * SelectedCoursesCookie
 *  .load(this.$cookies)
 *  .semester(semester)
 *  .addCourse(course)
 *  .save()
 */
class FinalsPageCookie {
  /**
   * @typedef finalExam
   * @property {string} Department
   * @property {string} CourseCode
   * @property {string} Section
   * @property {string} Day
   *
   *
   * @typedef SelectedExams
   * @type {{[semester: string]: SelectedExams[]}}
   */

  /**
   * @param {VueCookies} $cookies
   * @param {SelectedExams[]} selectedExams
   * @private
   */
  constructor($cookies, Exams) {
    /**
     * @type {VueCookies}
     * @private
     */
    this.$cookies = $cookies;
    /**
     * @type {finalExam}
     * @private
     */
    this._selectedExams = Exams;
    /**
     * @type {string}
     * @private
     */
    this.exam = undefined;
  }

  /**
   * Load saved selected courses from cookie
   * @param {VueCookies} $cookies
   * @param {string} key defaults to `COOKIE_KEY`
   * @returns {FinalsPageCookie}
   */
  static load($cookies, key = COOKIE_KEY) {
    return new FinalsPageCookie(
      $cookies,
      $cookies.isKey(key) ? $cookies.get(key) : {}
    );
  }

  /**
   * Save current state into cookie
   * @param {string} key defaults to `COOKIE_KEY`
   */
  save(key = COOKIE_KEY) {
    this.$cookies.set(key, this._selectedExams);
  }

  /**
   * Reset state to empty. Useful for resetting cookie
   *
   * @example SelectedCoursesCookie.load(this.$cookies).clear().save()
   */
  clear() {
    this._selectedExams = {};

    return this;
  }

  /**
   *
   * @returns {SelectedCourse[]} list of selected courses
   * of current semester
   */
  get selectedCourses() {
    if (this._semester === undefined) {
      return [];
    }

    if (this._selectedSemesters[this._semester] === undefined) {
      this._selectedSemesters[this._semester] = [];
    }

    return this._selectedSemesters[this._semester];
  }

  /**
   * Shouldn't be called outside of this instance
   * @private
   */
  set selectedCourses(newSelectedCourses) {
    if (this._semester === undefined) {
      return;
    }

    this._selectedSemesters[this._semester] = newSelectedCourses;
  }

  /**
   * Returns selectedCourse entry corresponding to `id`.
   * If entry does not exist, create new entry for `id`
   * @param {string} id ID of course
   * @returns {Course}
   */
  getSelectedCourse(id) {
    const selectedCourse = this.selectedCourses.find(
      (selectedCourse) => selectedCourse.id === id
    );

    if (selectedCourse === undefined) {
      const newSelectedCourse = { id, selectedSectionCrns: [] };

      this.selectedCourses.push(newSelectedCourse);

      return newSelectedCourse;
    } else {
      return selectedCourse;
    }
  }

  /**
   * Only adds an entry for the course, to add sections, call `addCourseSection`
   * @param {Course} course
   * @returns {this}
   */
  addCourse(course) {
    this.getSelectedCourse(course.id);

    return this;
  }

  /**
   * @param {Course} course
   * @param {CourseSection} section
   * @returns {this}
   */
  addCourseSection(course, section) {
    this.getSelectedCourse(course.id).selectedSectionCrns.push(section.crn);
    return this;
  }

  /**
   * @param {Course} course
   * @returns {this}
   */
  removeCourse(course) {
    this.selectedCourses = this.selectedCourses.filter(
      (selectedCourse) => selectedCourse.id !== course.id
    );

    return this;
  }

  /**
   *
   * @param {CourseSection} section
   * @returns {this}
   */
  removeCourseSection(section) {
    const selectedCourse = this.selectedCourses.find((selectedCourse) =>
      selectedCourse.selectedSectionCrns.some((crn) => crn === section.crn)
    );

    selectedCourse.selectedSectionCrns = selectedCourse.selectedSectionCrns.filter(
      (crn) => crn !== section.crn
    );

    return this;
  }
}

export { FinalsPageCookie };
