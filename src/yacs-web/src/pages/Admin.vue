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
            uploadCsv(formData).then(response => {
                let filename = formData.get("file").name;
                if (response.status === 200) {
                    this.$bvToast.toast(`${filename} has been successfully uploaded!`, {
                        title: "Upload Result",
                        variant: "info",
                        noAutoHide: false
                    });
                }
                else {
                    console.log(response);
                    this.$bvToast.toast(`${filename} hasn't been successfully uploaded.`, {
                        title: "Upload Result",
                        variant: "danger",
                        noAutoHide: true
                    });
                }
                this.loading = false;
            })
            .catch(error => {
                this.loading = false;
                this.$bvToast.toast(`${error}`, {
                    title: "Upload Result",
                    variant: "danger",
                    noAutoHide: true
                });
            });
        }
    },
    created() {

    }
}
</script>