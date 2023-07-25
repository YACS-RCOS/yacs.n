import "@/typedef";

// eslint-disable-next-line no-unused-vars
import {VueCookies} from "vue-cookies";

const COOKIE_KEY = "finalExams";

class FinalsPageCookie {
    // /**
    //  * @param {VueCookies} $cookies
    //  * @private
    //  */
    constructor($cookies) {
        this.$cookies = $cookies;
        this.exams = [];
    }
    // constructor($cookies, exams) {
    //     this.$cookies = $cookies;
    //     this.exams = exams; // Initialize as empty array
    // }


    // /**
    //  * @param {VueCookies} $cookies
    //  //* @param {string} key defaults to `COOKIE_KEY`
    //  * @returns {FinalsPageCookie}
    //  */
    static load($cookies) {// key = COOKIE_KEY
        // console.log("load: ", this.getExams());
        return new FinalsPageCookie($cookies);
        // return new FinalsPageCookie(
        //     $cookies,
        //     $cookies.isKey(COOKIE_KEY) ? $cookies.get(COOKIE_KEY) : []
        // );
    }
    // static load($cookies) {
    //     const exams = $cookies.exams === null ? [] : $cookies.exams;
    //
    //     return new FinalsPageCookie($cookies, exams);
    // }

    /**
     * Save current state into cookie
     * @param {string} key defaults to `COOKIE_KEY`
     */
    save(key = COOKIE_KEY) {
        this.$cookies.set(key, this.exams);
    }

    clear() {
        this.exams = [];

        return this;
    }


    getExams() {
        return this.exams;
    }


    /**
     * Only adds an entry for the course, to add sections, call `addCourseSection`
     * @param {String} Department
     * @param {String} CourseCode
     * @param {String} Section
     * @param {String} Day
     * @returns {this}
     */
    addCourse(Department, CourseCode, Section, Day) {
        console.log(this.exams);

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
}

export {
    FinalsPageCookie
};
