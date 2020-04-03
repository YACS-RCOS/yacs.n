<template>
    <b-container>
        <section id="import-data">
            <h2>Set Default Semester</h2>
            <div class="well well-sm">
            </div>
            <form @submit="onUpdate" class="form-group" method="post">
                <label for="semester">Select default Semester: &nbsp;</label>
                <select v-model="semester">
                  <option v-for="sem in semesterOptions" v-bind:value="sem.value" v-bind:key="sem.text">
                    {{ sem.text }}
                  </option>
                </select>
                <br />
                <input type="Submit" class="btn btn-success btn-sm" value="Submit" />
            </form>
        </section>
        <b-spinner v-show="loading" />
    </b-container>
</template>

<script>
import { updateSemester } from '@/services/AdminService';
import { getDefaultSemester } from '@/services/AdminService';
import { getSemesters } from '@/services/YacsService';

export default {
    name: "SetDefault",
    components: {},
    props: {},
    data () {
        return {
            loading: false,
            semester: '',
            semesterOptions: []
        };
    },
    methods: {
        onUpdate(event){
          event.preventDefault();
          this.loading = true;
          updateSemester(this.semester)
            .then(response => {
                console.log(response);
                // Axios will only enter this block if the status code is 2xx,
                // so handle errors for catch block. https://stackoverflow.com/questions/49967779/axios-handling-errors
                this.$bvToast.toast(`${this.semester} has been set as default`, {
                  title: 'Update Result',
                  variant: 'info',
                  noAutoHide: false
                });
                this.loading=false;
              })
              .catch(error => {
                console.log(error.response);
                this.$bvToast.toast(`HTTP ${error.response.status}: ${error.response.data}`, {
                  title: 'Update Result',
                  variant: 'danger',
                  noAutoHide: true
                });
                this.loading=false;
              });
        },
        back() {
            window.history.back();
        }
    },
    created() {
      // assign semester to current semester
      getDefaultSemester()
        .then(semester => {
          this.semester = semester
        })
      // create options for updating default
      getSemesters()
        .then(semesters => {
          this.semesterOptions.push(...semesters.map(s => ({text: s.semester, value: s.semester})));
        });
    },
}
</script>

<style lang="scss" scoped>

</style>
