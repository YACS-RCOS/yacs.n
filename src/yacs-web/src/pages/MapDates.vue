<template>
    <b-container>
        <section id="import-data">
            <h2>Assign Semester Part Name to Date Ranges</h2>
            <form @submit.prevent="onSubmit">
                <b-container
                    v-for="(standardSemesterName, key) in standardSemesterNames"
                    :key="key"
                    fluid
                >
                    <h3>{{ standardSemesterName }}</h3>
                    <hr />
                    <b-table
                        :id="`edit${standardSemesterName.replace(' ', '')}Tbl`"
                        :items="subsemesters.filter(x => x.semester_name === standardSemesterName)"
                        :per-page="perPage"
                        :current-page="currentPage"
                        :fields="displayedColumns"
                    >
                        <template v-slot:cell(dateRange)="data">
                            {{ formatDateRange(data.item.date_start, data.item.date_end) }}
                        </template>
                        <template v-slot:cell(semesterPartName)="data">
                            <input type="text" class="form-control" :placeholder="data.item.display_string" name="semester_part_name" />
                        </template>
                    </b-table>
                    <b-pagination
                        v-model="currentPage"
                        :total-rows="subsemesters.filter(x => x.semester_name === standardSemesterName).length"
                        :per-page="perPage"
                        :aria-controls="`edit${standardSemesterName.replace(' ', '')}Tbl`"
                    />
                </b-container>
                <button type="submit" class="btn btn-primary mt-2">Submit</button>
            </form>
        </section>
    </b-container>
</template>

<script>
import { mapDateRangeToSemesterPart as postDateMapping } from '@/services/AdminService';
import { getSubSemesters } from '@/services/YacsService';
import { readableDate } from '../utils';

export default {
    name: "MapDates",
    props: {},
    components: {},
    data () {
        return {
            perPage: 3,
            currentPage: 1,
            subsemesters: [],
            displayedColumns: ['dateRange', 'semesterPartName'],
            standardSemesterNames: []
        }
    },
    methods: {
        onSubmit(event) {
            let formData = new FormData(event.target);
            postDateMapping(formData).then(res => {
                console.log(res);
            });
        },
        formatDateRange(date1, date2) {
            return `${readableDate(date1)} - ${readableDate(date2)}`;
        }
    },
    created() {
        getSubSemesters().then(subsemesters => {
            this.subsemesters = subsemesters;
            this.standardSemesterNames = new Set(subsemesters.map(subsemester => subsemester.semester_name));
        });
    }
}
</script>

<style lang="scss">

</style>