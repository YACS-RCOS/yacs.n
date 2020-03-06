<template>
    <b-container>
        <h1>Admin Panel</h1>
        <hr>
        <h2>Import Data</h2>
        <section id="import-data">
        <div class="well well-sm">
            Input course data as CSV, for more info, see: <a href=#>http://help.com</a> (show github link for more docs later)
        </div>
        <form action="http://localhost:5000/api/courses" method="POST" enctype="multipart/form-data" class="form-group">
            <input type="file" name="file" class="form-control-file"> <br>
            <input type="Submit" class='btn btn-success btn-sm' value="Submit">
        </form>
        </section>
        <hr>
    </b-container>
</template>

<script>
export default {
    name: "AdminPage",
    components: {

    },
    data() {
        return {}
    },
    created() {

    }
}
</script>