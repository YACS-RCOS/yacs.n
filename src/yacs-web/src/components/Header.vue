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
        <b-navbar-nav class="ml-auto">
            <div>
            <b-button v-b-modal.modal-1>Login</b-button>

            <b-modal id="modal-1" ref="modal-1" hide-footer title="Login">
                <!-- <p class="my-4">Hello from modal!</p> -->
                <div>
                    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
                    <b-form-group
                        id="input-group-1"
                        label="Email address:"
                        label-for="input-1"
                        description="We'll never share your email with anyone else."
                    >
                        <b-form-input
                        id="input-1"
                        v-model="form.email"
                        type="email"
                        required
                        placeholder="Enter email"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
                        <b-form-input
                        id="input-2"
                        v-model="form.name"
                        required
                        placeholder="Enter name"
                        ></b-form-input>
                    </b-form-group>

                    <b-button type="submit" variant="primary">Submit</b-button>
                    <b-button type="reset" variant="danger">Reset</b-button>
                    </b-form>
                    <b-card class="mt-3" header="Form Data Result">
                    <pre class="m-0">{{ form }}</pre>
                    </b-card>
                </div>       
      
                <b-button class="mt-2"  block @click="toggleModal">Toggle Me</b-button>                     
            </b-modal>
            </div>
        </b-navbar-nav>


    </b-navbar>

</template>

<script>
import { getSemesters } from '@/services/YacsService';
import { getSemester } from '@/services/AdminService';

export default {
    name: 'Header',
    data() {
      return {
        form: {
          email: '',
          name: '',
        },
        show: true,
        selectedSemester: null,
			  semesterOptions: []
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
    },
    methods: {
      toggleModal() {
        // We pass the ID of the button that we want to return focus to
        // when the modal has hidden
        this.$refs['modal-1'].hide()
      },        
      onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.form))
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.name = ''
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }    
}
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
