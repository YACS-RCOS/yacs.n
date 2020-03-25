<template>
    <section id="MapDateRangeToName">
        <h2>Assign Semester Part Name to Date Ranges</h2>
        <form @submit.prevent="onSubmit" class="text-center">
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
                        <input type="hidden" name="date_start" :value="standardDate(data.item.date_start)" />
                        <input type="hidden" name="date_end" :value="standardDate(data.item.date_end)" />
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
                    align="fill"
                />
            </b-container>
            <button type="submit" :class="{
                'btn': true,
                'btn-primary': true,
                'my-2': true,
                'w-50': true,
                'success': success,
                'fail': fail
            }"
            @animationend="resetIndicators"
            >
                Submit <b-spinner v-show="loading" />
            </button>
        </form>
    </section>
</template>

<script>
import { mapDateRangeToSemesterPart as postDateMapping } from '@/services/AdminService';
import { getSubSemesters } from '@/services/YacsService';
import { readableDate, standardDate } from '../utils';

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
            standardSemesterNames: [],
            loading: false,
            success: false,
            fail: false
        }
    },
    methods: {
        onSubmit(event) {
            if (!this.loading) {
                this.loading = true;
                let formData = new FormData(event.target);
                postDateMapping(formData).then(res => {
                    console.log(res);
                    this.success = true;
                })
                .catch(error => {
                    console.log(error);
                    this.fail = true;
                })
                .finally(() => {
                    this.loading = false;
                });
            }
        },
        formatDateRange(date1, date2) {
            return `${readableDate(date1)} - ${readableDate(date2)}`;
        },
        standardDate,
        resetIndicators() {
            this.fail = false;
            this.success = false;
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
$danger:     #dc3545;
$success:   #28a745;
$primary:    #007bff;

.success {
    animation: success ease-in-out 2s;
}

.fail {
    animation: fail ease-in-out 2s;
}

@keyframes success {
    50% {
        background-color: $success;
    }
    to {
        background-color: $primary;
    }
}

@keyframes fail {
    50% {
        background-color: $danger;
    }
    to {
        background-color: $primary;
    }
}
</style>