<template>
    <div>
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
                <b-form-select 
                    v-model="selectedDepartment" 
                    :options="departmentOptions"
                ></b-form-select>
            </b-form-group>
        </div>

        <hr>

        <b-list-group class="course-list" flush>
            <b-list-group-item
                button
                v-for="course in filteredCourses"
                :key="course.name + course.date_end + course.date_start"
                :disabled="course.selected"
                :class="{'bg-light': course.selected}"
                @click="$emit('addCourse', course)"
            >
                <b>{{ course.name }}</b> ({{ readableDate(course.date_start) }} - {{ readableDate(course.date_end) }}) <br>
                {{ course.title }}
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<script>
import { TimeDateMixin } from '@/mixins';

import {
    getCourses,
    getDepartments,
    getSubSemesters
} from '@/services/YacsService';

export default {
    name: 'CourseList',
    mixins: [
        TimeDateMixin
    ],
    data () {
        return {
            textSearch: null,
            selectedSubsemester: null,
            subsemesterOptions: [{text: 'All', value: null}],
            selectedDepartment: null,
            departmentOptions: [{text: 'All', value: null}],
            courses: [],
        }
    },
    created () {
        getCourses().then(courses => this.courses.push(...courses));
        getDepartments().then(departments => {
            this.departmentOptions.push(...departments.map(d => d.department));
        });
        getSubSemesters().then(subsemesters => {
            this.subsemesterOptions.push(...subsemesters.map(subsemester => {
                return {text: subsemester.display_string, value: subsemester};
            }));
        });
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

<style>

</style>