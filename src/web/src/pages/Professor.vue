<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

    <!-- button to switch between alphabet order and category order -->
    <div style="float: left;" class="w-10">
      <b-button
        @click="listAlphabet()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >
        List by Alphabet
      </b-button>
      <br />
      <b-button
        @click="listCate()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >
        List by Department
      </b-button>
    </div>
    <div v-if="categories.length > 0" class="mx-auto w-75">
      <!-- pop-up window -->
      <b-modal ref="my-modal">
        <div class="block text-left" v-if="showPath != null" md="10">
          <h3
            class="text-center"
            style="color: #007bff; margin-top: -5px; margin-bottom: 5px;"
          >
            {{ showPath.Name[0] }}
          </h3>
          <br />
          <div v-for="(item, itemName) in showPath" :key="itemName">
            <h4 style="color: #3395ff; margin-top: -20px;">
              {{ itemName + ": " }}
            </h4>
            <li
              v-for="course in item"
              :key="course"
              v-on:click="goPage(course)"
              class="courseInPath"
            >
              {{ course }}
            </li>
            <br />
          </div>
        </div>
      </b-modal>

      <b-row>
        <!-- splitted categories into 2 arrays, so we can have 2 columns -->
        <b-col
          v-for="(catCol, index) in categoryCols"
          :key="`catCol-${index}`"
          md="6"
          v-show="cateShow"
        >
          <b-row
            v-for="categoryObj in catCol"
            :key="categoryObj['Department Name'][0]"
            class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Category Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ categoryObj["Department Name"][0] }}
                </h3>
              </b-row>
              <!-- professor Names  -->
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the professor department list -->
                  <div
                    v-for="professor in categoryObj['Professors']"
                    :key="professor['Name'][0]"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <!-- professor button -->
                      <b-button
                        @click="ShowPath(professor)"
                        squared
                        variant="light"
                        class="professor-button m-0 ml-1"
                      >
                        {{ professor["Name"][0] }}
                      </b-button>
                    </div>
                  </div>
                </div>
              </b-row>
            </b-col>
          </b-row>
        </b-col>

        <!-- splitted professors in alphabet order -->
        <b-col
          v-for="(alphCol, index) in alphabetCols"
          :key="`alphCol-${index}`"
          md="6"
          v-show="alphShow"
        >
          <b-row
            v-for="alphabetObj in alphCol"
            :key="alphabetObj['Department Name'][0]"
            class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Alphabet Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ alphabetObj["Department Name"][0] }}
                </h3>
              </b-row>
              <!-- professor Names  -->
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the professor Alphabet list -->
                  <div
                    v-for="professor in alphabetObj['Professors']"
                    :key="professor['Name'][0]"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <!-- professor button -->
                      <b-button
                        @click="ShowPath(professor)"
                        squared
                        variant="light"
                        class="professor-button m-0 ml-1"
                      >
                        {{ professor["Name"][0] }}
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
import json from "./Professor_Data.json";
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  name: "Professors",
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
      categories: json,
      showPath: null,
      cateShow: true,
      alphShow: false,
    };
  },
  computed: {
    // splitted categories into 2 arrays, one array = one column
    categoryCols() {
      let ret = [];
      let col1 = [];
      let col2 = [];
      for (var i = 0; i < this.categories.length; i++) {
        if (i < this.categories.length / 2) {
          col1.push(this.categories[i]);
        } else {
          col2.push(this.categories[i]);
        }
      }
      ret.push(col1);
      ret.push(col2);
      return ret;
    },

    // splitted professors to alphabet categories, then splitted categories into 2 arrays, one array = one column
    alphabetCols() {
      let cols = [];
      // put all professors in one array
      for (var i = 0; i < this.categories.length; i++) {
        for (var j = 0; j < this.categories[i]["Professors"].length; j++) {
          cols.push(this.categories[i]["Professors"][j]);
        }
      }

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
      var half_length = Math.ceil(cols.length / 2);
      var count = 0;
      // splitted professors to alphabet categories, then splitted categories into 2 arrays
      for (var n = 0; n < alphabet.length; n++) {
        var tmp = {
          "Department Name": alphabet[n],
          Professors: [],
        };
        for (var m = 0; m < cols.length; m++) {
          if (cols[m]["Name"][0].startsWith(alphabet[n])) {
            var index = 0;
            while (index < tmp["Professors"].length) {
              if (cols[m]["Name"][0] < tmp["Professors"][index]["Name"][0]) {
                break;
              }
              index++;
            }
            tmp["Professors"].splice(index, 0, cols[m]);
          }
        }
        // splitted categories into 2 arrays
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
  },
  methods: {
    listAlphabet() {
      this.cateShow = false;
      this.alphShow = true;
    },
    listCate() {
      this.cateShow = true;
      this.alphShow = false;
    },
    // Display a pop-up window when a professor is clicked
    ShowPath(professor) {
      console.log(this.$refs["my-modal"]);
      console.log(professor);
      this.showPath = professor;
      this.$refs["my-modal"].show();
    },
    // Go to the course page when a course inside the pop-up window is clicked
    goPage(course) {
      var subject = "" + course[0] + course[1] + course[2] + course[3];
      var courseID = "" + course[5] + course[6] + course[7] + course[8];
      if (course[4] != " ") {
        return;
      }
      if (course[8] == "X") {
        this.$router.push("/explore/" + subject);
      } else {
        this.$router.push(
          "/explore/" + subject + "/" + subject + "-" + courseID
        );
      }
    },
  },
};
</script>

<style>
.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}

.categoryBox {
  text-align: center;
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
  text-align: justify;
  width: 95%;
}

.professor-button:hover {
  background: rgba(108, 90, 90, 0.15) !important;
}

.courseInPath {
  cursor: pointer;
}

.courseInPath:hover {
  background-color: rgba(39, 130, 230, 0.5);
}
</style>
