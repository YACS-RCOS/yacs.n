<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

    <!-- button to switch between alphabet order and department order -->
    <div class="filter-buttons w-10" style="float: left;">
      <b-button @click="listAlphabet()"> 
        List by Alphabet 
      </b-button>
      <b-button @click="listDepartment()"> 
        List by Department 
      </b-button>
    </div>

    <div v-if="professors.length > 0" class="mx-auto w-75">
      <!-- pop-up window -->
      <b-modal ref="my-modal">
        <div class="block text-left" v-if="showProf != null" md="10">
          <h3
            class="text-center"
            style="color: #007bff; margin-top: -5px; margin-bottom: 5px;"
          >
            {{ showProf.Name }}
          </h3>
          <br />
          <div v-for="(item, itemName) in showProf" :key="itemName">
            <h4
              v-if="itemName != 'Name'"
              style="color: #3395ff; margin-top: -20px;"
            >
              {{ itemName + ": " }}
            </h4>
            <h5 v-if="itemName != 'Name'" :key="item" class="profInfo">
              {{ item }}
            </h5>
            <br />
          </div>
        </div>
      </b-modal>

      <b-row>
        <!-- split departments into 2 arrays, so we can have 2 columns -->
        <b-col
          v-for="(deptCol, index) in departmentCols"
          :key="`deptCol-${index}`"
          md="6"
          v-show="deptShow"
        >
          <b-row
            v-for="deptObj in deptCol"
            :key="deptObj['Department']"
            class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Category Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ deptObj["Department"] }}
                </h3>
              </b-row>
              <!-- Pathway Names  -->
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the Pathway Categories list -->
                  <div
                    v-for="prof in deptObj['Professors']"
                    :key="prof['Name']"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <!-- professor button -->
                      <b-button
                        @click="goPage(prof)"
                        squared
                        variant="light"
                        class="professor-button m-0 ml-1"
                      >
                        {{ prof["Name"] }}
                      </b-button>
                    </div>
                  </div>
                </div>
              </b-row>
            </b-col>
          </b-row>
        </b-col>

        <!-- split professors into alphabet order -->
        <b-col
          v-for="(alphCol, index) in alphabetCols"
          :key="`alphCol-${index}`"
          md="6"
          v-show="alphShow"
        >
          <b-row
            v-for="alphabetObj in alphCol"
            :key="alphabetObj['Letter']"
            class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Alphabet Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ alphabetObj["Letter"] }}
                </h3>
              </b-row>
              <!-- Professor Names  -->
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the Professor Alphabet list -->
                  <div
                    v-for="prof in alphabetObj['Professors']"
                    :key="prof['Name']"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <!-- professor button -->
                      <b-button
                        @click="goPage(prof)"
                        squared
                        variant="light"
                        class="professor-button m-0 ml-1"
                      >
                        {{ prof["Name"] }}
                      </b-button>
                    </div>
                  </div>
                </div>
              </b-row>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </div>
    <CenterSpinner
      v-else
      :height="80"
      :fontSize="1.3"
      loadingMessage="Professors"
      :topSpacing="30"
    />
  </b-container>
</template>

<script>
import json from "./Professors.json";
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  name: "Professor",
  components: {
    CenterSpinner: CenterSpinnerComponent,
  },
  data() {
    return {
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Professors",
        },
      ],
      professors: json,
      showProf: null,
      deptShow: false,
      alphShow: true,
    };
  },
  computed: {
    departmentCols() {
      // create list of departments
      var half_length = Math.ceil(this.professors.length / 2);
      var count = 0;
      var departments = [];
      var dept = "";
      for (let i = 0; i < this.professors.length; i++) {
        dept = this.professors[i]["Department"];
        if (dept == "") {
          dept = this.professors[i]["Portfolio"];
        }
        if (!departments.includes(dept)) {
          departments.push(dept);
        }
      }
      departments.sort();

      let ret = [];
      let col1 = [];
      let col2 = [];
      for (var i = 0; i < departments.length; i++) {
        var tmp = {
          Department: departments[i],
          Professors: [],
        };
        for (var j = 0; j < this.professors.length; j++) {
          dept = this.professors[j]["Department"];
          if (dept == "") {
            dept = this.professors[i]["Portfolio"];
          }
          var name = this.professors[j]["Name"];
          var last_name = name.split(" ").slice(-1)[0];
          if (dept == departments[i]) {
            var index = 0;
            while (index < tmp["Professors"].length) {
              if (
                last_name <
                tmp["Professors"][index]["Name"].split(" ").slice(-1)
              ) {
                break;
              }
              index++;
            }
            tmp["Professors"].splice(index, 0, this.professors[j]);
          }
        }

        // sort by last name, then first name
        tmp["Professors"].sort((a, b) => {
          if (
            a["Name"].split(" ").slice(-1)[0] ===
            b["Name"].split(" ").slice(-1)[0]
          ) {
            return a["Name"].split(" ")[0] < b["Name"].split(" ")[0] ? -1 : 1;
          } else {
            return a["Name"].split(" ").slice(-1)[0] <
              b["Name"].split(" ").slice(-1)[0]
              ? -1
              : 1;
          }
        });

        // split departments into 2 arrays
        if (tmp["Professors"].length > 0) {
          if (count < half_length) {
            col1.push(tmp);
            count += tmp["Professors"].length + 0.2;
          } else {
            col2.push(tmp);
          }
        }
      }
      ret.push(col1);
      ret.push(col2);
      return ret;
    },
    // split professors into alphabet groups, then split groups into 2 columns
    alphabetCols() {
      var half_length = Math.ceil(this.professors.length / 2);
      var count = 0;
      let alphabet = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
      ];

      let ret = [];
      let col1 = [];
      let col2 = [];
      for (var i = 0; i < alphabet.length; i++) {
        var tmp = {
          Letter: alphabet[i],
          Professors: [],
        };
        for (var j = 0; j < this.professors.length; j++) {
          var name = this.professors[j]["Name"];
          var last_name = name.split(" ").slice(-1)[0];
          if (last_name.startsWith(alphabet[i])) {
            tmp["Professors"].push(this.professors[j]);
          }
        }

        // sort by last name, then first name
        tmp["Professors"].sort((a, b) => {
          if (
            a["Name"].split(" ").slice(-1)[0] ===
            b["Name"].split(" ").slice(-1)[0]
          ) {
            return a["Name"].split(" ")[0] < b["Name"].split(" ")[0] ? -1 : 1;
          } else {
            return a["Name"].split(" ").slice(-1)[0] <
              b["Name"].split(" ").slice(-1)[0]
              ? -1
              : 1;
          }
        });

        // split into 2 arrays
        if (tmp["Professors"].length > 0) {
          count += tmp["Professors"].length + 0.2;
          if (count < half_length) {
            col1.push(tmp);
          } else {
            col2.push(tmp);
          }
        }
      }
      ret.push(col1);
      ret.push(col2);
      return ret;
    },
  },

  methods: {
    listAlphabet() {
      this.deptShow = false;
      this.alphShow = true;
    },
    listDepartment() {
      this.deptShow = true;
      this.alphShow = false;
    },
    // Display a pop-up window when a professor is clicked
    ShowProf(professor) {
      console.log(this.$refs["my-modal"]);
      console.log(professor);
      this.showProf = professor;
      this.$refs["my-modal"].show();
    },
    // Go to the professor page when a professor is clicked
    goPage(professor) {
      console.log(professor);
      var rcs = professor["Email"].replace("@rpi.edu", "");
      this.$router.push("/professor/" + rcs);
    },
  },
};
</script>

<style>

.filter-buttons {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.filter-buttons button {
  color: #007bff;
  border: solid #007bff;
  background-color: transparent;
  width: 100%;
}

.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}

.category-title {
  color: hsl(211, 100%, 60%);
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}

.professor-button {
  display: inline-block;
  background: white;
  border-style: none;
  text-align: left;
  width: 95%;
  padding-top: 0;
  padding-bottom: 0;
}

.professor-button:hover {
  background: rgba(108, 90, 90, 0.15) !important;
}

.h3 {
  text-align: left;
}

@media (max-width: 768px) {
  .filter-buttons {
    /* in mobile mode move filters above professors so mobile view doesn't get smushed */
    float: none;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
    gap: 5px;
  }
}
</style>
