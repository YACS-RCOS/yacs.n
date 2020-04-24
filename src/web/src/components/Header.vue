<template>
  <div id="header">
    <b-navbar type="light" variant="light">
      <b-navbar-brand class="logo" href="#">YACS</b-navbar-brand>
      <div class="semester">{{currentSemester}}</div>
      <!-- If user has logged in -->
      <b-navbar-nav class="ml-auto" v-if="sessionID!==null">
        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>Hi, {{ userName }}</template>
          <!-- <b-dropdown-item href="#">Profile</b-dropdown-item> -->
          <b-dropdown-item @click="logOut">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>

      <!-- If user has not logged in -->
      <b-navbar-nav class="ml-auto" v-if="sessionID===null">
        <div>
          <b-button v-b-modal.modal-1 size="sm" variant="light">Log In</b-button>

          <b-button v-b-modal.singup-modal size="sm" variant="primary" class="ml-2">Sign Up</b-button>

          <b-modal id="modal-1" ref="modal-1" hide-footer title="Log In">
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

              <!-- <b-button :pressed.sync="showSignUp" variant="primary" id="signUpButton">Sign Up</b-button> -->
            </b-form>

            <div v-if="showSignUp">
              <SignUpForm></SignUpForm>
              <b-button :pressed.sync="showSignUp" variant="primary">Go back to Log In</b-button>
            </div>
          </b-modal>

          <b-modal id="singup-modal" ref="singup-modal" hide-footer title="Sign Up">
            <SignUpForm></SignUpForm>
          </b-modal>
        </div>
      </b-navbar-nav>
    </b-navbar>
    <hr />
  </div>
</template>

<script>
import { login, logout } from '@/services/UserService';

import SignUpComponent from '@/components/SignUp';

export default {
  name: 'Header',
  props: {
    semester: String
  },
  components: {
    SignUpForm: SignUpComponent
  },
  data() {
    return {
      form: {
        email: '',
        password: ''
      },

      isLoggedIn: false,
      showSignUp: false,
      sessionID: '',
      userName: '',
      show: true,
      semesterOptions: []
    };
  },
  computed: {
    // When you assign a data var to a prop, the data var does not change on prop update (seems this is intended behavior)
    // use computed instead to get current semester which reflects one in parent component.
    // https://forum.vuejs.org/t/update-data-when-prop-changes-data-derived-from-prop/1517/15
    currentSemester() {
      return this.semester;
    }
  },
  created() {
    this.sessionID = this.$cookies.get('sessionID');
    this.userName = this.$cookies.get('userName');
    if (this.sessionID == '') {
      console.log('not logged in');
    } else {
      console.log('sessionID', this.sessionID);
    }
  },
  methods: {
    toggleModal() {
      this.$refs['modal-1'].hide();
    },
    onSubmit(evt) {
      evt.preventDefault();
      let userInfo = this.form;
      console.log(userInfo);

      login(userInfo)
        .then(response => {
          console.log(response);
          this.$cookies.set('sessionID', response.data.content['sessionID']);
          this.$cookies.set('userName', response.data.content['userName']);
          this.$cookies.set('userID', response.data.content['uid']);
          location.reload();
        })
        .catch(error => {
          console.log(error.response);
          this.$bvToast.toast(`Login Unsuccesful. Please double check your email and password, then try again!`, {
                  title: 'Invalid login',
                  variant: 'danger',
                  noAutoHide: true
                });
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
        var sessionId = this.$cookies.get("sessionID");
        logout(sessionId).then(() => {
          this.$cookies.remove("sessionID");
          this.$cookies.remove("userID");
          location.reload();
        });
      }

    }
  }

</script>

<style>
.navbar {
  background: white !important;
  margin-bottom: none !important;
}

.semester {
  font-size: 18px;
  color: grey;
}

.logo {
  font-size: 24px;
  vertical-align: middle;
}

hr {
  margin: 0em;
  border-width: 1px;
}

#signUpButton {
  margin-left: 20px;
}
</style>
