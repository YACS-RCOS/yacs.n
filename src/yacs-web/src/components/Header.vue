<template>
    <b-navbar type="light" variant="light">
        <b-navbar-brand class = "logo" href="#">YACS</b-navbar-brand>

		<b-form-select label= "semester" class="semesters" v-model="selectedSemester" :options="semesterOptions">
			<template v-slot:first>
				<b-form-select-option :value="null" disabled>-- Please select a semester --</b-form-select-option>
			</template>
		</b-form-select>
    </b-navbar>
</template>

<script>
import {
    getSemesters
} from '../services/YacsService';

export default {
  name: 'Header'
};
</script>

<style></style>
