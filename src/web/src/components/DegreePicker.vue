<template>
  <div>
    <b-form-group id="degreeinput" label="Degree:">
      <b-form-select
        v-model="currentdegree"
        :disabled="!loaded"
        :options="degrees"
        required
        @change="currentmajor = [null]"
        @input="check"
      ></b-form-select>
    </b-form-group>

    <b-form-group id="majorinput" label="Major:">
      <div v-for="(thing, i) in this.currentmajor" :key="i">
        <b-form-select
          :ref="'majorpicker' + i"
          :disabled="!loaded"
          :value="thing"
          required
          @blur.native="setmajor(i,$refs['majorpicker' + i][0].$el.value)"
        >
          <b-form-select-option
            v-for="(major, j) in majors[degree]"
            :key="j"
            :disabled="major.disabled && (major.selectedfor != i)"
            :value="major.value"
          >
            {{ major.text }}
          </b-form-select-option>
        </b-form-select>
      </div>
      <b-button
        :disabled="currentmajor==null || currentmajor.length <= 1"
        @click="currentmajor.pop()"
      >
        <font-awesome-icon :icon="faMinus" class="m-auto"/>
      </b-button>
      <b-button
        @click="currentmajor.push(null);"
      >
        <font-awesome-icon :icon="faPlus" class="m-auto"/>
      </b-button>
    </b-form-group>
  </div>
</template>

<script>
import { getMajors } from "@/services/AdminService";
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";

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
      majors: {
        null: [{ text: "Select a degree type first", value: null }],
      },
      reversemajors: {},
      loaded: false,
      placeholder: placeholder,
      faMinus: faMinus,
      faPlus: faPlus
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
      //store majors in an array
      (response) => {
        this.majors[this.degrees[1]] = [this.placeholder].concat(response.data["B"].map((val) => {
          return { text: val, value: val }
        }));
        this.majors[this.degrees[2]] = [this.placeholder].concat(
          response.data["M"].map((val) => {
            return { text: val, value: val }
          }),
          response.data["D"].map((val) => {
            return { text: val, value: val }
          })
        );

        //create reverse lookup table
        this.reversemajors[this.degrees[1]] = []
        this.reversemajors[this.degrees[2]] = []

        this.majors[this.degrees[1]].forEach((val, index) => {
          this.reversemajors[this.degrees[1]][val.text] = index;
        });
        this.majors[this.degrees[2]].forEach((val, index) => {
          this.reversemajors[this.degrees[2]][val.text] = index;
        });
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
    check() {
      this.$nextTick().then(() => {
        if(this.loaded) {
          for(var i in this.currentmajor) {
            if(!this.$refs['majorpicker' + i][0].$el.checkValidity()) {
              this.$set(this.currentmajor, i, null);
            }
            this.setmajor(i, this.currentmajor[i])
          }
        }
      });
    },
    setmajor(index, value) {
      if(this.degree == null) {
        return;
      }

      let val = (value.length > 0) ? value : null;

      var oldindex = this.reversemajors[this.degree][this.currentmajor[index]]
      var oldentry = this.majors[this.degree][oldindex]

      var newindex = this.reversemajors[this.degree][val]
      var newentry = this.majors[this.degree][newindex]

      if(oldentry && oldentry.value) {
        this.$set(oldentry, "disabled", false);
        this.$set(oldentry, "selectedfor", -1);
      }
      if(newentry && newentry.value) {
        this.$set(newentry, "disabled", true);
        this.$set(newentry, "selectedfor", index);
      }

      this.$set(this.currentmajor, index, val);
    },
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
</script>


<style scoped>

#majorinput button {
  margin: 1em 0.1em;
  /*width: 2em;*/
}

#majorinput select {
  margin: 0.4em 0 0;
}

</style>