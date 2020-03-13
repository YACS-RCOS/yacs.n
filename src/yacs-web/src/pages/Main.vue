<template>
    <b-container fluid class="pt-3">
        <Header></Header>
        <b-row>
            <b-col md="4">
               
                <!-- <h3>{{Header.selectedSemester}}</h3> -->
                <hr>

                <div class="course-search">
                    <b-form-group
                        label="Search"
                        label-for="search"
                    >
                        <b-form-input id="search" v-model="textSearch" trim placeholder="Intro to College - COLG 1030 - 5/2"></b-form-input>
                    </b-form-group>

                    <b-form-group
                        label="Filter Sub-Semester"
                        for="sub-semester"
                    >
                        <b-form-select v-model="selectedSubsemester" :options="subsemesterOptions"></b-form-select>
                    </b-form-group>

                    <b-form-group
                        label="Filter Department"
                        for="department"
                    >
                        <b-form-select v-model="selectedDepartment" :options="departmentOptions"></b-form-select>
                    </b-form-group>
                </div>

                <hr>

                <b-list-group class="course-list" flush>
                    <b-list-group-item
                        v-for="course in filteredCourses"
                        :key="course.name + course.date_end + course.date_start"
                        :disabled="course.selected"
                        :class="{'bg-light': course.selected}"
                        @click="addCourse(course)"
                    >
                        <b>{{ course.name }}</b> ({{ readableDate(course.date_start) }} - {{ readableDate(course.date_end) }}) <br>
                        {{ course.title }}
                    </b-list-group-item>
                </b-list-group>

            </b-col>
            <b-col md='8'>
                <Schedule :courses="selectedCourses" :courseIdentifierFunc="_getCourseIdentifier" @unselectCourse="removeCourse"></Schedule>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import {
    getCourses,
    getDepartments,
    getSubSemesters
} from '../services/YacsService';

import Header from '../components/Header';

import Schedule from '../components/Schedule';

export default {
    name: 'MainPage',
    components: {
        Header,
        Schedule
    },
    data () {
        return {
            textSearch: null,
            selectedSubsemester: null,
            subsemesterOptions: [{text: 'All', value: null}],
            selectedDepartment: null,
            departmentOptions: [{text: 'All', value: null}],
            courses: [],
            selectedCourses: {},
        }
    },
    created () {
        getCourses().then(({ data }) => {
            this.courses = data.map(c => {
                c.date_start = new Date(c.date_start);
                c.date_end = new Date(c.date_end);
                c.str = [c.title, c.name, this.readableDate(c.date_start), this.readableDate(c.date_end)].join();

                c.sections = c.sections.filter(s => !!s);
                c.sections.forEach(s => {if (s) s.selected = false;});
                c.selected = false;
                return c;
            });
        });
        getDepartments().then(({ data }) => {
            this.departmentOptions.push(...data.map(d => ({text: d.department, value: d.department})));
        });
        getSubSemesters().then(({ data }) => {
            this.subsemesterOptions.push(...data.map(subsemester => {
                subsemester.date_start = new Date(subsemester.date_start)
                subsemester.date_end = new Date(subsemester.date_end)
                subsemester.date_start_display = this.readableDate(subsemester.date_start);
                subsemester.date_end_display = this.readableDate(subsemester.date_end);

                const text = `${subsemester.date_start_display} - ${subsemester.date_end_display}`;

                return {text, value: subsemester};
            }));
        });
    },
    methods: {
        readableDate (date) {
            return `${date.getMonth() + 1}/${date.getDate()}`;
        },
        _getCourseIdentifier(courseObj) {
            return `${courseObj.department}${courseObj.level}${courseObj.date_start.getMonth() + 1}${courseObj.date_start.getDay() + 1}${courseObj.date_start.getFullYear()}${courseObj.date_end.getMonth() + 1}${courseObj.date_end.getDay() + 1}${courseObj.date_end.getFullYear()}`;
        },
        addCourse (course) {
            console.log(`Adding ${course.title} to selected courses`);
            console.log(course);
            course.selected = true;
            // This must be vm.set since we're adding a property onto an object
            this.$set(this.selectedCourses, this._getCourseIdentifier(course), course);
        },
        removeCourse (course) {
            this.$delete(this.selectedCourses, this._getCourseIdentifier(course));
            course.selected = false;
        }
    },
    computed: {
        filteredCourses () {
            return this.courses.filter(({date_start, date_end, department, str}) => {
                return (!this.selectedSubsemester ||
                        (this.selectedSubsemester.date_start.getTime() === date_start.getTime() &&
                        this.selectedSubsemester.date_end.getTime() === date_end.getTime()))
                        && (!this.selectedDepartment ||
                            this.selectedDepartment === department)
                        && (!this.textSearch || str.includes(this.textSearch.toUpperCase()));
            });
        }
    }
}
</script>

<style scoped lang="scss">
.course-list > div.list-group-item:hover {
    background-color: #DDD;
    cursor: pointer;
}
</style>
