<template>
    <form
        class="my-5 text-center"
        ref="editSemesterForm"
        @submit.prevent="onSubmit"
    >
        <h3>{{ semesterTitle }}</h3>
        <hr />
        <b-table
            :id="`edit${semesterTitle.replace(' ', '')}Tbl`"
            :items="subsemesters"
            :fields="displayedColumns"
        >
            <template v-slot:cell(dateRange)="data">
                {{ formatDateRange(data.item.date_start, data.item.date_end) }}
                <input type="hidden" name="date_start" :value="standardDate(data.item.date_start)" />
                <input type="hidden" name="date_end" :value="standardDate(data.item.date_end)" />
            </template>
            <template v-slot:cell(semesterPartName)="data">
                <input
                    type="text"
                    class="form-control"
                    name="semester_part_name"
                    :old-name="data.item.display_string"
                    :placeholder="data.item.display_string"
                    @input="checkIfValidName"
                />
            </template>
        </b-table>
        <button type="submit"
            :class="{
                'btn': true,
                'btn-primary': true,
                'my-2': true,
                'w-50': true,
                'no-cursor': disableSubmit
            }"
            @animationend="removeFeedbackClasses($event.target)"
            :disabled="disableSubmit"
        >
            Update <b-spinner class="d-none" />
        </button>
    </form>
</template>

<script>
import { mapDateRangeToSemesterPart as postDateMapping } from '@/services/AdminService';
import { standardDate } from '@/utils';

export default {
    name: "EditSemesterDateNameBinding",
    props: {
        semesterTitle: String,
        subsemesters: Array
    },
    data () {
        return {
            displayedColumns: ['dateRange', 'semesterPartName'],
            loading: false,
            disableSubmit: true
        }
    },
    methods: {
        onSubmit(event) {
            if (!this.loading) {
                let submitBtn = event.target.querySelector("button[type='submit']");
                let spinner = submitBtn.querySelector("span.spinner-border");
                // Stop any current animation if user clicks while it's happening
                this.removeFeedbackClasses(submitBtn);
                this.loading = true;
                spinner.classList.remove("d-none");
                let formData = new FormData(event.target);
                postDateMapping(formData).then(res => {
                    console.log(res);
                    submitBtn.classList.add("success");
                })
                .catch(error => {
                    console.log(error);
                    submitBtn.classList.add("fail");
                })
                .finally(() => {
                    spinner.classList.add("d-none");
                    this.loading = false;
                });
            }
        },
        removeFeedbackClasses(btn) {
            btn.classList.remove("success");
            btn.classList.remove("fail");
        },
        /***
         * @param {Date} date1
         * @param {Date} date2
         * @returns {String} date of the form "MM/DD/YYYY - MM/DD/YYYY"
        */
        formatDateRange(date1, date2) {
            return `${date1.toLocaleDateString()} - ${date2.toLocaleDateString()}`;
        },
        checkIfValidName (event) {
            // Disable if the value is falsey,
            // or if it's the same value as before
            console.log(event.target)
            console.log(event.target.value)
            console.log(event.target.getAttribute("old-name"))
            console.log(event.target.value === event.target.getAttribute("old-name"))
            this.disableSubmit = !event.target.value || event.target.value === event.target.getAttribute("old-name");
        },
        standardDate,
    }
}
</script>

<style lang="scss" scoped>
.no-cursor {
    cursor: not-allowed;
}
</style>