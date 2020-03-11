<template>
    <b-container>
        <h1>Admin Panel</h1>
        <hr>
        <section id="import-data">
            <h2>Import Data</h2>
            <div class="well well-sm">
                Input course data as CSV, for more info, see: <a href=#>http://help.com</a> (show github link for more docs later)
            </div>
            <form @submit="onSubmit" class="form-group">
                <input type="file" name="file" class="form-control-file"> <br>
                <input type="Submit" class='btn btn-success btn-sm' value="Submit">
            </form>
        </section>
        <a @click="back" class="btn btn-info text-white">Back</a>
        <b-spinner v-show="loading" />
        <hr>
    </b-container>
</template>

<script>
import { uploadCsv } from "../services/AdminService";

export default {
    name: "AdminPage",
    components: {

    },
    data() {
        return {
            loading: false
        }
    },
    methods: {
        onSubmit(event) {
            event.preventDefault();
            let formData = new FormData(event.target);
            this.loading = true;
            if (formData.get("file") && formData.get("file").name) {
                let filename = formData.get("file").name;
                uploadCsv(formData).then(response => {
                    console.log(response);
                    // Axios will only enter this block if the status code is 2xx,
                    // so handle errors for catch block. https://stackoverflow.com/questions/49967779/axios-handling-errors
                    this.$bvToast.toast(`${filename} has been successfully uploaded!`, {
                        title: "Upload Result",
                        variant: "info",
                        noAutoHide: false
                    });
                    this.loading = false;
                })
                .catch(error => {
                    console.log(error.response);
                    this.loading = false;
                    this.$bvToast.toast(`HTTP ${error.response.status}: ${error.response.data}`, {
                        title: "Upload Result",
                        variant: "danger",
                        noAutoHide: true
                    });
                });
            }
            else {
                this.$bvToast.toast(`Must upload a CSV file`, {
                    title: "Validation Error",
                    variant: "danger",
                    noAutoHide: false
                });
                this.loading = false;
            }
        },
        back() {
            window.history.back();
        }
    },
    created() {

    }
}
</script>