import "@/typedef";

// eslint-disable-next-line no-unused-vars
import {VueCookies} from "vue-cookies";

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
        this._semester = undefined;
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
     * @returns {SelectedExams[]} list of selected courses
     * of current semester
     */
    get selectedExams() {
        if (this._semester === undefined) {
            return [];
        }

        if (this._selectedExams[this._semester] === undefined) {
            this._selectedExams[this._semester] = [];
        }

        return this._selectedExams[this._semester];
    }

    /**
     * Shouldn't be called outside of this instance
     * @private
     */
    set selectedExams(newSelectedExams) {
        if (this._semester === undefined) {
            return;
        }

        this._selectedExams[this._semester] = newSelectedExams;
    }

    /**
     * Returns selectedCourse entry corresponding to `id`.
     * If entry does not exist, create new entry for `id`
     * @param {string} Department ID of course
     * @param {string} CourseCode
     * @param {string} Section
     * @param {string} Day
     * @returns {FinalExam}
     */
    getSelectedCourse(Department, CourseCode, Section, Day) {
        const selectedExam = this.selectedExams.find(
            (selectedExam) => selectedExam.Department === Department && selectedExam.CourseCode === CourseCode
                && selectedExam.Section === Section && selectedExam.Day === Day
        );

        if (selectedExam === undefined) {
            const newSelectedExam = {Department, CourseCode, Section, Day, selectedSectionExams: []};

            this.selectedExams.push(newSelectedExam);

            return newSelectedExam;
        } else {
            return selectedExam;
        }
    }

    /**
     * Only adds an entry for the course, to add sections, call `addCourseSection`
     * @param {string} Department
     * @param {string} CourseCode
     * @param {string} Section
     * @param {string} Day
     * @returns {this}
     */
    addCourse(Department, CourseCode, Section, Day) {
        this.getSelectedCourse(Department, CourseCode, Section, Day);

        return this;
    }

    /**
     * Adds a section to the selected course.
     * @param {string} Department ID of the course department.
     * @param {string} CourseCode Code of the course.
     * @param {string} Section Section of the course.
     * @param {string} Day Day of the course.
     * @returns {this}
     */
    addCourseSection(Department, CourseCode, Section, Day) {
        const selectedExam = this.getSelectedCourse(Department, CourseCode, Section, Day);
        selectedExam.selectedSectionExams.push({Department, CourseCode, Section, Day});
        return this;
    }

    /**
     * Removes a course from the selected courses.
     * @param {string} Department ID of the course department.
     * @param {string} CourseCode Code of the course.
     * @param {string} Section Section of the course.
     * @param {string} Day Day of the course.
     * @returns {this}
     */
    removeCourse(Department, CourseCode, Section, Day) {
        this.selectedExams = this.selectedExams.filter(
            (selectedExam) => !(selectedExam.Department === Department && selectedExam.CourseCode === CourseCode && selectedExam.Section === Section && selectedExam.Day === Day)
        );
        return this;
    }


    /**
     * Removes a section from the selected course.
     * @param {string} Department ID of the course department.
     * @param {string} CourseCode Code of the course.
     * @param {string} Section Section of the course.
     * @param {string} Day Day of the course.
     * @returns {this}
     */
    removeCourseSection(Department, CourseCode, Section, Day) {
        const selectedExam = this.selectedExams.find((selectedExam) =>
            selectedExam.Department === Department && selectedExam.CourseCode === CourseCode && selectedExam.Section === Section && selectedExam.Day === Day
        );

        if (selectedExam) {
            selectedExam.selectedSectionExams = [];
        }

        return this;
    }

}

export {FinalsPageCookie};
