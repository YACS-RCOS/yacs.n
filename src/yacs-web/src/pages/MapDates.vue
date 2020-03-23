<template>
    <b-container>
        <section id="import-data">
            <h2>Assign Date Ranges to Semester Parts</h2>
            <form @submit.prevent="onSubmit">
                <b-form-group>
                    <legend>
                        Date range
                    </legend>
                    <label class="d-block">
                        Select Start Date
                        <b-form-datepicker name="date_start" local="en" />
                    </label>
                    <label class="d-block">
                        Select End Date
                        <b-form-datepicker name="date_end" local="en" />
                    </label>
                    <label class="d-block">
                        Semester Part Name
                        <input type="text" class="form-control" name="semester_part_name" />
                    </label>
                </b-form-group>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </section>
    </b-container>
</template>

<script>
import { mapDateRangeToSemesterPart as postDateMapping } from '@/services/AdminService';

export default {
    name: "MapDates",
    props: {},
    components: {},
    data () {
        return {}
    },
    methods: {
        onSubmit() {
            let formData = new FormData(event.target);
            postDateMapping(formData).then(res => {
                console.log(res);
            });
        }
    }
}
</script>

<style lang="scss">

</style>