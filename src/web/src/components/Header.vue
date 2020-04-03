<template>
  <div id='header'>
    <b-navbar type="light" variant="light">
        <b-navbar-brand class="logo"  href="#">YACS</b-navbar-brand>
        <div class="semester"> {{currentSemester}} </div>
        <b-navbar-nav class="ml-auto" v-if="sessionID!==null">
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              {{ sessionID }}
            </template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item @click="logOut">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>          
          
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto" v-if="sessionID===null">
            <div>
            <b-button v-b-modal.modal-1 size="sm" variant="light">Log In</b-button>

            <b-modal id="modal-1" ref="modal-1" hide-footer title="Log In">
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

                    <b-form-group id="input-group-2" label="Password:" label-for="input-2">
                        <b-form-input
                        id="input-2"
                        type="password"
                        v-model="form.password"
                        required
                        placeholder="Enter password"
                        ></b-form-input>
                    </b-form-group>                    

                    <b-button type="submit" variant="primary">Submit</b-button>
                    <b-button type="reset" variant="danger">Reset</b-button>
                    </b-form>

                    <!-- <b-card class="mt-3" header="Form Data Result">
                    <pre class="m-0">{{ form }}</pre>
                    </b-card> -->

                </div>

                <!-- <b-button class="mt-2"  block @click="toggleModal">Toggle Me</b-button> -->
            </b-modal>
            </div>
        </b-navbar-nav>

      </b-navbar>
      <hr>
    </div>
</template>

<script>
import { getDefaultSemester } from '@/services/AdminService';
import { login } from '@/services/UserService';

export default {
    name: 'Header',
    data() {
      return {
        form: {
          email: '',
          password: '',
        },
        isLoggedIn: false,
        sessionID: '',
        show: true,
        semesterOptions: [],
        currentSemester: ''
      }
    },
    created(){
      if(this.$route.query.semester){
        this.currentSemester = this.$route.query.semester;
      }
      else{
        getDefaultSemester().then(semester => {
          this.currentSemester = semester;
        });
      }
      this.sessionID = this.$cookies.get("sessionID");
      if (this.sessionID == '') {
        console.log('not logged in');
      } else {
        console.log('sessionID', this.sessionID);
      }
    },
    methods: {
      toggleModal() {
        // We pass the ID of the button that we want to return focus to
        // when the modal has hidden
        this.$refs['modal-1'].hide()
      },
      onSubmit(evt) {
        evt.preventDefault()
        let userInfo = this.form;
        console.log(userInfo);
        
        login(userInfo)
        .then(response => {
          console.log(response);
          this.$cookies.set("sessionID", response.data.content['sessionID']);
          location.reload();
        })
        .catch(error => {
          console.log(error.response);
        });
        this.toggleModal();
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.email = 'aaa1@wa.com'
        this.form.password = '123456'
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      },
      logOut(){
        this.$cookies.remove("sessionID");
        location.reload();
      }
    
    }
}
</script>

<style>
.navbar {
  background: white !important;
  margin-bottom: none !important;
}

.semester{
  font-size: 18px;
  color: grey;
}

.logo{
  font-size: 24px;
  vertical-align: middle;
}

hr {
  margin: 0em;
  border-width: 1px;
}

</style>
