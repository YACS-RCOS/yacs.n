`
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
      <div v-for="(thing, i) in this.currentmajor" :key="i">
        <b-form-select
          :ref="'majorpicker' + i"
          :disabled="!loaded"
          :options="majorslist[i]"
          :value="thing"
          required
          @blur.native="currentmajor[i] = $refs['majorpicker' + i][0].localValue; refresh()"
        ></b-form-select>
        <!--the @input is used to keep focus since it disappears for some reason-->
      </div>
      <b-button
        variant=""
        @click="currentmajor.push(null)"
      >+
      </b-button>
      <b-button
        :disabled="currentmajor==null || currentmajor.length <= 1"
        @click="currentmajor.pop()"
      >-
      </b-button>


    </b-form-group>
  </div>
</template>

<script>
import { getMajors } from "@/services/AdminService";

export default {
  name: "DegreePicker",
  props: {
    degree: String,
    major: Array[String],
  },
  emits: ["update:degree", "update:major"],
  data() {
    let placeholder = { text: "Select one...", value: null };
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
    if(this.currentmajor == '') {
      this.currentmajor = [null];
    }
    if(this.currentdegree == '') {
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
    log(x) {
      console.log(x)
      return x
    },
    refresh() {
      //hack to force vue to see that the value changed
      var temp = this.currentmajor;
      this.currentmajor = null;
      this.$nextTick(() => {
        this.currentmajor = temp;
      });
    },
    check() {
      this.$nextTick().then(() => {
        if(this.loaded) {
          var refresh = false
          for(var i in this.currentmajor) {
            if(this.majorslist[0].indexOf(this.currentmajor[i]) == -1) {
              refresh = true;
              this.currentmajor[i] = null;
            }
          }
          if(refresh) {
            this.refresh();
          }
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
        if(this.loaded) {
          return this.major;
        } else {
          return null;
        }

      },
      set(val) {
        this.$emit("update:major", val);
      }
    },
    majorslist: {
      get() {
        if(!this.loaded) {
          return [{ text: "Loading...", value: null, disabled: true }];
        } else {
          let i = this.degrees.indexOf(this.currentdegree);
          var ans = [];
          for(var j = 0; j < this.nummajors; j++) {
            var temp = Object.assign([], this.majors[(i > -1) ? i : 0]);
            for(var k = 0; k < this.nummajors; k++) {
              if(k == j){
                continue;
              }
              var prev = temp.indexOf(this.currentmajor[k]);
              temp[prev] = { text: this.currentmajor[k], disabled: true };
            }
            ans.push(temp)
          }
          // console.log(ans)
          return ans;
        }

      }
    },
    nummajors: {
      get() {
        if(this.currentmajor != null) {
          return this.currentmajor.length;
        }
        return 0;
      }
    }
  }
};
</script>`