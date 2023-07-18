import "@/typedef";

// eslint-disable-next-line no-unused-vars
import {VueCookies} from "vue-cookies";

const COOKIE_KEY = "finalExams";

class FinalsPageCookie {

    constructor($cookies) {
        this.$cookies = $cookies;
        this.exams = [];
        this._semester = undefined;
    }

    static load($cookies, key = COOKIE_KEY) {
        return new FinalsPageCookie(
            $cookies,
            $cookies.isKey(key) ? $cookies.get(key) : {}
        );
    }

    save(key = COOKIE_KEY) {
        this.$cookies.set(key, this.exams);
    }

    clear() {
        this.exams = {};

        return this;
    }

    getExams() {
        return this.exams;
    }


    addCourse(Department, CourseCode, Section, Day) {
        const course = {
            Department,
            CourseCode,
            Section,
            Day,
        };
        this.exams.push(course);
        this.save();
        return this;
    }

    //
    // /**
    //  * Removes a course from the selected courses.
    //  * @param {string} Department ID of the course department.
    //  * @param {string} CourseCode Code of the course.
    //  * @param {string} Section Section of the course.
    //  * @param {string} Day Day of the course.
    //  * @returns {this}
    //  */
    // removeCourse(Department, CourseCode, Section, Day) {
    //     this.selectedExams = this.selectedExams.filter(
    //         (selectedExam) => !(selectedExam.Department === Department && selectedExam.CourseCode === CourseCode && selectedExam.Section === Section && selectedExam.Day === Day)
    //     );
    //     return this;
    // }


}

export {FinalsPageCookie};
