<template>
  <div>
    <b-form-group id="degreeinput" label="Degree:">
      <b-form-select
        v-model="currentdegree"
        :disabled="!loaded"
        :options="degrees"
        required
        @input="check"
      ></b-form-select>
    </b-form-group>

    <b-form-group id="majorinput" label="Major:">
      <b-form-select
        v-model="currentmajor"
        :disabled="!loaded"
        :options="majorslist"
        required
      ></b-form-select>
    </b-form-group>
  </div>
</template>

<script>
import { getMajors } from "@/services/AdminService";

export default {
  name: "DegreePicker",
  props: {
    degree: String,
    major: String
  },
  emits: ["update:degree", "update:major"],
  data() {
    let placeholder =  { text: "Select one...", value: null };
    return {
      degrees: [
        placeholder,
        "Undergraduate",
        "Graduate"
      ],
      majors: [
        [{ text: "Select a degree type first", value: null }],
        [],
        []
      ],
      loaded: false,
      placeholder: placeholder,
    };
  },
  mounted() {
    if(this.currentmajor == ''){
      this.currentmajor = null;
    }
    if(this.currentdegree == ''){
      this.currentdegree = null;
    }

    getMajors().then(
      (response) => {
        this.majors[1] = [this.placeholder].concat(response.data["B"]);
        this.majors[2] = [this.placeholder].concat(response.data["M"], response.data["D"]);

      },
      (errMsg) => {
        this.$bvToast.toast(errMsg.response.data || "Unknown Error", {
          title: "Loading majors failed!",
          variant: "danger",
          noAutoHide: true
        });
      }
    ).then(() => {
      this.loaded = true;
      this.check();
    })
    ;
  },
  methods: {
    check() {
      this.$nextTick().then(() => {
        if (this.loaded && this.majorslist.indexOf(this.currentmajor) == -1) {
          this.currentmajor = null;
        }
      });
    }
  },
  computed: {
    currentdegree: {
      get() {
        return this.degree;
      },
      set(val) {
        this.$emit("update:degree", val);
      }

    },
    currentmajor: {
      get() {
        if (this.loaded) {
          return this.major;
        } else {
          return null;
        }

      },
      set(val) {
        this.$emit("update:major", val);
      }

    },
    majorslist() {
      if (!this.loaded) {
        return [{ text: "Loading...", value: null, disabled: true }];
      } else {
        let i = this.degrees.indexOf(this.currentdegree);
        return this.majors[(i > -1) ? i : 0];
      }

    }
  }
};
</script>