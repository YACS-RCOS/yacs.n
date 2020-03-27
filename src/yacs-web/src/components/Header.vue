<template>
  <b-navbar type="light" variant="light">
    <b-navbar-brand class="logo" href="#">YACS - {{selectedSemester}}</b-navbar-brand>

    <b-form-select
      label="semester"
      class="semesters"
      v-model="selectedSemester"
      :options="semesterOptions"
    >
      <template v-slot:first>
        <b-form-select-option :value="null" disabled>-- Please select a semester --</b-form-select-option>
      </template>
    </b-form-select>
  </b-navbar>
</template>

<script>
import { getSemesters } from '@/services/YacsService';
import { getSemester } from '@/services/AdminService';

export default {
  name: 'Header',
    data () {
        return {
			selectedSemester: null,
			semesterOptions: [],
        }
    },
    created () {
		getSemesters().then(({ data }) => {
            this.semesterOptions.push(...data.map(s => ({text: s.semester, value: s.semester})));
            //this.selectedSemester = getSemester()
            
        });
    getSemester().then(({data}) => {
            this.selectedSemester = data.semester;
        });
    }
};
</script>

<style>
.semesters{
	position: absolute;
	right: 0;
	width: 50%;
	padding-right: 5px;
}
.semester{
	font-size: 18px;
	vertical-align: middle;
}
.logo{
	font-size: 24px;
	vertical-align: middle;
}

</style>
