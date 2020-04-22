<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          required
          placeholder="Enter email"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Full Name:" label-for="input-2">
        <b-form-input id="input-2" v-model="form.name" required placeholder="Enter name"></b-form-input>
      </b-form-group>

      <!-- <b-form-group id="input-group-3" label="Phone Number:" label-for="input-3">
        <b-form-input id="input-3" v-model="form.phone" required placeholder="Enter your phone number"></b-form-input>
      </b-form-group> -->

      <b-form-group id="input-group-4" label="Password:" label-for="input-4">
        <b-form-input type="password" id="input-4" v-model="form.password" required placeholder="Enter your password"></b-form-input>
      </b-form-group>      

      <b-form-group id="input-group-5" label="Degree:" label-for="input-5">
        <b-form-select
          id="input-5"
          v-model="form.degree"
          :options="degrees"
        ></b-form-select>
      </b-form-group>

      <b-form-group id="input-group-6" label="Major:" label-for="input-6">
        <b-form-input id="input-6" v-model="form.major" placeholder="Eg. CSCI or ITWS"></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>

<script>

import { login, signup } from '@/services/UserService';
export default {
  name: 'SignUp',
  data() {
    return {
      form: {
        email: '',
        name: '',
        phone: '',
        password: '',
        degree: '',
        major: ''
      },
      degrees: [{ text: 'Select One', value: null }, 'Undergraduate', 'Graduate'],
      show: true
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      // alert(JSON.stringify(this.form));
      signup(this.form).then((response)=>{
        console.log(response);
        if (response.data.content){
          alert(response.data.content['msg'])
          
          login({'email' : this.form['email'], 'password': this.form['password']})
          .then(response => {
            console.log(response);
            this.$cookies.set('sessionID', response.data.content['sessionID']);
            this.$cookies.set('userName', response.data.content['userName']);
            this.$router.go()
          })
        } else {
          alert(response.data.errMsg)
        }
        
      })
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.email = '';
      this.form.name = '';
      this.form.food = null;
      this.form.checked = [];
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    }
  }
};
</script>
