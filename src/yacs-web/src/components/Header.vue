<template>
  <b-navbar type="light" variant="light">
    <b-navbar-brand class="logo" href="#">YACS</b-navbar-brand>

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
import { getSemesters } from '../services/YacsService';

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
            this.selectedSemester = this.semesterOptions[0].value;
            
        });
    },

    watch: {
    	selectedsemester: function(val, oldVal){
    		this.$emit('new-semester', val);
    		console.log("Semester changed from", oldVal, "to", val);

    	}
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
