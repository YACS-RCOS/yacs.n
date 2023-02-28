<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-container v-if="isLoggedIn" id="user-info-box" class="border">
      <h1 class="text-center">Hi, {{ user.name }}!</h1>
      <b-row v-for="(data, label) in userData" :key="label" class="user-row">
        <b-form inline style="width: 100%" @submit.prevent="finishedit(label, true)" @reset.prevent="finishedit(label,false)">
          <b-col class="user-col-left">
            {{ rendername(label) }}:
          </b-col>
          <template v-if="data.editing">
            <b-col class="user-col-center">
              <b-input
                :ref="label"
                v-model="currentinput[label]"
                :required="data.required"
                :type="data.type"
                autofocus
                @keydown.esc="finishedit(label,false)"
              ></b-input>
            </b-col>
            <b-col class="user-col-right">
              <b-button type="reset" variant="danger">Cancel</b-button>
              <b-button type="submit" variant="success">Done</b-button>
            </b-col>
          </template>
          <template v-else>
            <b-col class="user-col-center">
              <p :class="changed(label)">{{ rendervalue(form[label]) }}</p>
            </b-col>
            <b-col class="user-col-right">
              <b-button
                @click.prevent="startediting(label)"
              >Edit
              </b-button>
            </b-col>
          </template>
        </b-form>
      </b-row>
      <b-row class="user-row">
        <b-col class="user-col-left">
          Password:
        </b-col>
        <b-col class="user-col-center">
          <p :class="form.newpassword!=undefined?'user-changed-info':''">{{ form.newpassword != undefined ? renderpassword(form.newpassword) : "&lt;unchanged&gt;" }}</p>
        </b-col>
        <b-col class="user-col-right">
          <b-button v-b-modal.newpassword-modal>Edit</b-button>
        </b-col>
      </b-row>
      <b-row class="user-row">
        <b-col class="user-col-left">
          Current Degree:
        </b-col>
        <b-col class="user-col-center">
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
        <b-button class="align-self-center m-auto" style="width: 10em" variant="danger" @click="onReset">Reset Changes</b-button>
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
import { modifyUser } from "@/services/UserService";

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
    newpasswordmodalHandleevent(bvModalEvent) {
      if(bvModalEvent.trigger == "ok") {
        this.form.newpassword = this.currentinput.newpassword.length == 0 ? undefined : this.currentinput.newpassword;
      }
      this.currentinput.newpassword = "";
    },
    onReset() {
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
        return;
      } else {
        this.$bvToast.toast("Your information has been updated.", {
          title: "Updating user information success",
          variant: "success"
        });
        this.form.newpassword = undefined;
        this.$store.commit(userTypes.mutations.SET_USER_INFO, this.form);
        this.$refs["login-modal"].hide();
        return;
      }
    }
  }
};
</script>

<style scoped>
#user-info-box {
  padding: 1em;
  margin-top: 2em;
  margin-bottom: 2em;
  width: 50%;
  min-width: max-content;

}

#user-info-box .user-row {
  padding: 0.2em;
  margin: 0.2em 0em;
}

#user-info-box .user-row .col {
  /*min-width: max-content;*/
  /*width: 33%;*/
  min-height: 2.5em;
}

#user-info-box .user-row .user-col-left {
  justify-content: right;
}

#user-info-box .user-row .user-col-center {
  justify-content: center;
  display: grid;
}

#user-info-box .user-row .user-col-center .degreelabel {
  display: block;
  text-align: center;
}

#user-info-box .user-row .user-col-right {
  justify-content: left;
}

#user-info-box .user-row .user-col-right * {
  margin-right: 1em;
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