<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-container v-if="isLoggedIn" id="user-info-box">
      <h1 class="text-center">Hi, {{ user.name }}!</h1>
      
      <b-row class="user-row">
        <b-col class="user-col-left">
          <p style="font-weight: bold;">Name:</p>
        </b-col>
      </b-row>
      <b-row class="user-row">
        <b-form inline style="width: 100%" @submit.prevent="finishedit('name', true)" @reset.prevent="finishedit('name', false)">
          <b-col class="user-col-left" v-if="!userData.name.editing">
            <b-input
            :ref="user.name"
            v-model="currentinput.name"
            @click.prevent="startediting('name')"
            style="border: 1px solid #ccc; padding: 5px; width: 100%; cursor: pointer;"
            ></b-input>         
          </b-col>
          <b-col class="user-col-left" v-else>
            <b-input
              :ref="user.name"
              v-model="currentinput.name"
              :required="userData.name.required"
              :type="userData.name.type"
              autofocus
              @keydown.esc="finishedit('name', false)"
              style="border: 1px solid #ccc; width: 100%;"
            ></b-input>
          </b-col>
          <b-col class="user-col-right" v-if="userData.name.editing">
            <b-button type="reset" variant="danger" @click="finishedit('name', false)">Cancel</b-button>
            <b-button type="submit" variant="success" @click="finishedit('name', true)">Done</b-button>
          </b-col>
        </b-form>
      </b-row>

      <b-row class="user-row">
        <b-col class="user-col-left">
          <p style="font-weight: bold;">Email:</p>
        </b-col>
      </b-row>
      <b-row class="user-row">
        <b-form inline style="width: 100%" @submit.prevent="finishedit('email', true)" @reset.prevent="finishedit('email', false)">
          <b-col class="user-col-left" v-if="!userData.email.editing">
            <b-input
            :ref="user.email"
            v-model="currentinput.email"
            @click.prevent="startediting('email')"
            style="border: 1px solid #ccc; padding: 5px; width: 100%; cursor: pointer;"
            ></b-input>
          </b-col>
          <b-col class="user-col-left" v-else>
            <b-input
              :ref="user.email"
              v-model="currentinput.email"
              :required="userData.email.required"
              :type="userData.email.type"
              autofocus
              @keydown.esc="finishedit('email', false)"
              style="border: 1px solid #ccc; width: 100%;"
            ></b-input>
          </b-col>
          <b-col class="user-col-right" v-if="userData.email.editing" >
            <b-button type="reset" variant="danger" @click="finishedit('email', false)">Cancel</b-button>
            <b-button type="submit" variant="success" @click="finishedit('email', true)">Done</b-button>
          </b-col>
        </b-form>
      </b-row>

      <b-row class="user-row">
        <b-col class="user-col-left">
          <p style="font-weight: bold;">Phone Number:</p>
        </b-col>
      </b-row>
      <b-row class="user-row">
        <b-form inline style="width: 100%" @submit.prevent="finishedit('phone', true)" @reset.prevent="finishedit('phone', false)">
          <b-col class="user-col-left" v-if="!userData.phone.editing">
            <b-input
            :ref="user.phone"
            v-model="currentinput.phone"
            @click.prevent="startediting('phone')"
            style="border: 1px solid #ccc; padding: 5px; width: 100%; cursor: pointer;"
            ></b-input>
          </b-col>
          <b-col class="user-col-left" v-else>
            <b-input
              :ref="user.phone"
              v-model="currentinput.phone"
              :required="userData.phone.required"
              :type="userData.phone.type"
              autofocus
              @keydown.esc="finishedit('phone', false)"
              style="border: 1px solid #ccc; width: 100%;"
            ></b-input>
          </b-col>
          <b-col class="user-col-right" v-if="userData.phone.editing" >
            <b-button type="reset" variant="danger" @click="finishedit('phone', false)">Cancel</b-button>
            <b-button type="submit" variant="success" @click="finishedit('phone', true)">Done</b-button>
          </b-col>
        </b-form>
      </b-row>

      <b-row class="user-row">
        <b-col class="user-col-left">
          <p style="font-weight: bold;">Change Password:</p>
        </b-col>
      </b-row>
      <b-row class="user-row">
        <b-col class="user-col-left">
          <p :class="form.newpassword!=undefined?'user-changed-info':''">{{ form.newpassword != undefined ? renderpassword(form.newpassword) : "&lt;unchanged&gt;" }}</p>
        </b-col>
        <b-col class="user-col-right">
          <b-button v-b-modal.newpassword-modal>Edit</b-button>
        </b-col>
      </b-row>
      <b-row class="user-row">
        <b-col class="user-col-left">
          <p style="font-weight: bold;">Current Degree:</p>
        </b-col>
      </b-row>
      <b-row class="user-row">
        <b-col class="user-col-left">
          <div :class="changed('degree')" class="degreelabel">{{ form.degree }}</div>
          <div class="degreelabel">
            <div v-for="(name, i) in form.major" :key="name" :class="changed_major(i) +  ' degreelabel'">{{ name }}<br/></div>
          </div>
        </b-col>
        <b-col class="user-col-right">
          <b-button v-b-modal.degreepicker>Edit</b-button>
        </b-col>
      </b-row>
      <b-row style="margin-top: 1em">
        <b-button v-b-modal.delete class="align-self-center m-auto" style="width: 10em" variant="warning" >Delete Account</b-button>
        <b-button class="align-self-center m-auto" style="width: 10em" variant="danger" @click="onReset">Undo Changes</b-button>
        <b-button v-b-modal.login class="align-self-center m-auto" variant="success">Submit Changes...</b-button>
      </b-row>

    </b-container>
    <h1 v-else class="text-center">You should log in first.</h1>

    <b-modal id="degreepicker"
      cancel-variant="danger"
      ok-title="Done"
      ok-variant="success"
      size="xl"
      static
      title="Pick Degree and Major:"
      @cancel="degreemodalHandlecancel"
      @close="degreemodalHandlecancel"
      @hide="degreemodalHandlecancel"
      @ok="degreemodalHandleok">
      <b-form ref="degreeform">
        <degree-picker
          :degree="currentinput.degree"
          :major="currentinput.major"
          @update:degree="newval => currentinput.degree = newval"
          @update:major="newval => currentinput.major = newval"
        ></degree-picker>
      </b-form>
    </b-modal>
    <b-modal id="login"
      ref="login-modal"
      cancel-variant="danger"
      ok-title="Submit Changes"
      ok-variant="success"
      title="Please enter your password to continue"
      @hide="form.password = ''"
      @ok.prevent="loginmodalHandleok">
      <b-form ref="loginform" @submit.prevent="$refs['login-modal'].hide('ok')" @reset.prevent="$refs['login-modal'].hide('cancel')">
        <b-row>
          <b-col>
            <b-form-input
              v-model="form.password"
              autofocus
              required
              type="password"
            ></b-form-input>
          </b-col>
        </b-row>
      </b-form>
    </b-modal>
    <b-modal id="delete"
      ref="delete-modal"
      cancel-variant="secondary"
      ok-title="Delete Account"
      ok-variant="danger"
      title="Please enter your password to confirm account deletion"
      @hide="form.password = ''"
      @ok.prevent="deletemodalHandleok">
      <b-form ref="deleteform" @submit.prevent="$refs['delete-modal'].hide('ok')" @reset.prevent="$refs['delete-modal'].hide('cancel')">
        <b-row>
          <b-col>
            <b-form-input
              v-model="form.password"
              autofocus
              required
              type="password"
            ></b-form-input>
          </b-col>
        </b-row>
      </b-form>
    </b-modal>
    <b-modal id="newpassword-modal"
      ref="newpassword-modal"
      cancel-variant="danger"
      ok-title="Done"
      ok-variant="success"
      title="Please enter a new password"
      @hide="newpasswordmodalHandleevent">
      <b-form @submit.prevent="$refs['newpassword-modal'].hide('ok')" @reset.prevent="$refs['newpassword-modal'].hide('cancel')">
        <b-row>
          <b-col>
            <b-form-input
              v-model="currentinput.newpassword"
              autofocus
              type="password"
            ></b-form-input>
          </b-col>
        </b-row>
      </b-form>
    </b-modal>
  </b-container>
</template>

<script>
import { userTypes } from "@/store/modules/user";
import { mapGetters } from "vuex";
import DegreePicker from "@/components/DegreePicker";
import router from "@/routes";
import { modifyUser, deleteUser } from "@/services/UserService";
import {getStudentCourses} from "@/services/YacsService";
import store from '@/store';

export default {
  name: "User",
  components: { DegreePicker },
  data() {
    return {
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/"
        },
        {
          text: "User"
        }
      ],
      userData: {
        name: { type: "text", required: true, editing: false },
        email: { type: "email", required: true, editing: false },
        phone: { type: "tel", editing: false }
      },
      form: {}, //this will populate itself
      currentinput: {}
    };
  },
  mounted() {
    if(!this.isLoggedIn) {
      router.push("/");
    }
    this.onReset();
    getStudentCourses().then(response => {console.log(response)})
  },
  computed: {
    ...mapGetters({
      isLoggedIn: userTypes.getters.IS_LOGGED_IN,
      user: userTypes.getters.CURRENT_USER_INFO
    })
  },
  methods: {
    log(...val) {
      this.$nextTick(() => {
        console.log(val);
      });
    },
    rendername(value) {
      return value[0].toUpperCase() + value.substring(1);
    },
    renderpassword(value) {
      return "•".repeat(value.length);
    },
    rendervalue(value) {
      if(value === undefined || value.length == 0) {
        return "<not set>";
      } else {
        return value;
      }
    },
    changed(val) {
      return (this.user[val] != this.form[val]) ? "user-changed-info" : "";
    },
    changed_major(val) {
      return (this.form.major.length < this.user.major.length || val >= this.user.major.length || this.form.major[val] != this.user.major[val]) ? "user-changed-info" : "";
    },
    startediting(val) {
      this.userData[val].editing = true;
    },
    finishedit(val, good) {
      this.userData[val].editing = false;
      if(good) {
        this.form[val] = this.currentinput[val];
      } else {
        this.currentinput[val] = this.form[val];
      }
    },
    degreemodalHandleok(bvModalEvent) {
      if(this.$refs["degreeform"].checkValidity()) {
        this.form.degree = this.currentinput.degree;
        this.form.major = Object.assign([], this.currentinput.major);
      } else {
        bvModalEvent.preventDefault();
        this.$refs["degreeform"].reportValidity();
      }
    },
    degreemodalHandlecancel(bvModalEvent) {
      if(bvModalEvent.trigger != "ok") {
        this.currentinput.degree = this.form.degree;
        this.currentinput.major = Object.assign([], this.form.major);
      }
    },
    loginmodalHandleok() {
      if(this.$refs["loginform"].checkValidity()) {
        this.onSubmit();
      } else {
        this.$refs["loginform"].reportValidity();
      }
    },
    deletemodalHandleok() {
      if(this.$refs["deleteform"].checkValidity()) {
        this.onDelete();
      } else {
        this.$refs["deleteform"].reportValidity();
      }
    },
    newpasswordmodalHandleevent(bvModalEvent) {
      if(bvModalEvent.trigger == "ok") {
        this.form.newpassword = this.currentinput.newpassword.length == 0 ? undefined : this.currentinput.newpassword;
      }
      this.currentinput.newpassword = "";
    },
    onReset() {
      for(const key of Object.keys(this.userData)){
        this.userData[key]["editing"] = false;
      }
      this.form = JSON.parse(JSON.stringify(this.user));
      this.currentinput = JSON.parse(JSON.stringify(this.user));
    },
    async onSubmit() {
      this.form.sessionID = this.$store.state.user.sessionId;
      let {
        data: { success, errMsg }
      } = await modifyUser(this.form);

      if(!success) {
        this.$bvToast.toast(errMsg || "Unknown error", {
          title: "Updating user information failed",
          variant: "danger"
        });
      } else {
        this.$bvToast.toast("Your information has been updated.", {
          title: "Updating user information success",
          variant: "success"
        });
        this.form.newpassword = undefined;
        this.$store.commit(userTypes.mutations.SET_USER_INFO, this.form);
        this.$refs["login-modal"].hide();
      }
    },
    async onDelete() {
      this.form.sessionID = this.$store.state.user.sessionId;
      let {
        data: { success, errMsg }
      } = await deleteUser(this.form);

      if (!success) {
        this.$bvToast.toast(errMsg || "Unknown error", {
          title: "Account deletion failed",
          variant: "danger"
        });
      } else {
        store.dispatch(userTypes.actions.LOGOUT);
        this.$refs["delete-modal"].hide();
        this.$bvToast.toast("Your account has been deleted.", {
          title: "Account deletion success",
          variant: "success"
        });
      }
    },
  }
};
</script>

<style scoped>
#user-info-box {
  padding: 1em;
  margin-top: 2em;
  margin-bottom: 2em;
  width: 65%;
  min-width: max-content;
}

#user-info-box .user-row .col {
  min-height: 2.5em;
  display: flex;
  align-items: center;
}

#user-info-box .user-row .user-col-left {
  justify-content: left;
  font-size: large;
  flex: 0 0 65%;
}

#user-info-box .user-row .user-col-right {
  justify-content: right;
  flex: 0 0 35%;
}

#user-info-box .user-row .user-col-right b-input {
  border: 1px solid var(--primary);
}

#user-info-box .user-row .user-col-left b-input {
  border: 1px solid var(--primary);
}

#user-info-box .user-row .user-col-right * {
  margin-right: 1em;
}

#user-info-box .user-row .user-col-left .degreelabel {
  display: block;
  text-align: center;
  margin: 0.5em;
}

#user-info-box .user-row .user-changed-info {
  color: var(--warning);
}

#user-info-box .user-row * {
  text-align: center;
  display: flex;
  align-self: baseline;
}

</style>
