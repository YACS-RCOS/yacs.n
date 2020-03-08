<template>
    <b-container fluid class="pt-3">
        <b-row>
            <b-col md="4">
                <h3>YACS</h3>
                <hr>

                <div class="course-search">
                    <b-form-group
                        label="Search"
                        label-for="search"
                    >
                        <b-form-input id="search" v-model="textSearch" trim placeholder="Intro to College - COLG 1030 - 5/2"></b-form-input>
                    </b-form-group>
                <!-- <div class="form-group">
                    <label for="search">Search</label>
                    <input type="text" v-model='textSearch' class="form-control" id="search" placeholder="Intro to College - COLG 1030">
                </div> -->
                    <b-form-group
                        label="Filter Sub-Semester"
                        for="sub-semester"
                    >
                        <b-form-select v-model="selectedSubsemester" :options="subsemesterOptions"></b-form-select>
                    </b-form-group>
<!-- 
                <div class="form-group">
                    <label for="sub-semester">Filter Sub-Semester</label>
                    <select id='sub-semester' v-model='selectedSubsemester' class="form-control">
                    <option value="" selected>All</option>
                    <option ng-value="subsemester" ng-repeat='subsemester in subsemesters'>
                        {{subsemester.date_start_display}} - {{subsemester.date_end_display}}
                    </option>
                    </select>
                </div> -->
                    <b-form-group
                        label="Filter Department"
                        for="department"
                    >
                        <b-form-select v-model="selectedDepartment" :options="departmentOptions"></b-form-select>
                    </b-form-group>
                <!-- <div class="form-group">
                    <label for="department">Filter Department</label>
                    <select id='department' ng-model='departmentSearch' class="form-control">
                    <option value="" selected>All</option>
                    <option ng-value="department" ng-repeat='department in departments'>
                        {{department}}
                    </option>
                    </select>
                </div> -->
                </div>

                <hr>

                <b-list-group flush>
                    <b-list-group-item 
                        v-for="course in filteredCourses"
                        :key="course.name + course.date_end + course.date_start"
                        class="course-list-item"
                        @click="addCourse(course)"
                    >
                        <b>{{ course.name }}</b> ({{ readableDate(course.date_start) }} - {{ readableDate(course.date_end) }}) <br>
                        {{ course.title }}
                    </b-list-group-item>
                </b-list-group>

                <!-- <div class="course-list">
                    <div class="course-list-element" ng-repeat="class in classList | filter:textSearch | filter:{department: departmentSearch} | filter:subsemesterSearch(selectedSubsemester)">
                        <b>{{ class.name }} (4 Credits)</b>
                        <p> {{ class.title }} <i>by Professor Kuzmin</i></p>
                    </div>
                </div> -->

            </b-col>
            <b-col md='8'>
   
                <!-- <h3 class="text-center">Schedule</h3>
                <hr> -->
                <Schedule :courses="selectedCourses" @unselectCourse="removeCourse"></Schedule>
            </b-col>

            <!-- <div class="col-md-8">
            <h2 class="text-center">Schedule</h2>
            <hr>

            <div class="schedule"></div>
                <div class="div" ng-repeat='day in _schedule_template.days'>
                {{day}}
                <span class="div" ng-repeat='hour in _schedule_template.hours'>
                    {{day}}{{hour}}
                </span>
                <br>
                </div>

            </div> -->
        </b-row>
    </b-container>
</template>

<script>
import {
    getCourses,
    getDepartments,
    getSubSemesters
} from '../services/YacsService';

import Schedule from '../components/Schedule';

export default {
    name: 'MainPage',
    components: {
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
            selectedCourses: [],
        }
    },
    created () {
        getCourses().then(({ data }) => {
            this.courses = data.map(c => {
                c.date_start = new Date(c.date_start);
                c.date_end = new Date(c.date_end);
                c.str = [c.title, c.name, this.readableDate(c.date_start), this.readableDate(c.date_end)].join();
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
            return `${date.getMonth() + 1}/${date.getDay() + 1}`;
        },
        addCourse (course) {
            this.selectedCourses.push(course);
        },
        removeCourse (course) {
            this.selectedCourses.splice(this.selectedCourses.indexOf(course), 1);
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.course-list-item {
    cursor: pointer;
}
</style>
