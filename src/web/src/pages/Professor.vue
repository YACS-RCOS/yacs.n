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
        List by Category
      </b-button>
    </div>


    <div v-if="categories.length > 0" class="mx-auto w-75">
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
            :key="categoryObj['Category Name'][0]"
            class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Category Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ categoryObj["Category Name"][0] }}
                </h3>
              </b-row>
              <!-- Pathway Names  -->
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the Pathway Categories list -->
                  <div
                    v-for="pathway in categoryObj['Pathways']"
                    :key="pathway['Name'][0]"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <!-- pathway button -->
                      <b-button
                        @click="goPage(professor)"
                        squared
                        variant="light"
                        class="pathway-button m-0 ml-1"
                      >
                        {{ pathway["Name"][0] }}
                      </b-button>
                    </div>
                  </div>
                </div>
              </b-row>
            </b-col>
          </b-row>
        </b-col>

        <!-- splitted Pathways in alphabet order -->
        <b-col
          v-for="(alphCol, index) in alphabetCols"
          :key="`alphCol-${index}`"
          md="6"
          v-show="alphShow"
        >
          <b-row
            v-for="alphabetObj in alphCol"
            :key="alphabetObj['Category Name'][0]"
            class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Alphabet Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ alphabetObj["Category Name"][0] }}
                </h3>
              </b-row>
              <!-- Pathway Names  -->
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the Pathway Alphabet list -->
                  <div
                    v-for="pathway in alphabetObj['Pathways']"
                    :key="pathway['Name'][0]"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <!-- pathway button -->
                      <b-button
                        @click="ShowPath(pathway)"
                        squared
                        variant="light"
                        class="pathway-button m-0 ml-1"
                      >
                        {{ pathway["Name"][0] }}
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
      loadingMessage="Pathways"
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
      categories: [],
      professors: json,
      showProf: null,
      cateShow: false,
      alphShow: true,
    };
  },
  computed: {
    // splitted categories into 2 arrays, one array = one column
    categoryCols() {
      this.categories = Set();
      let ret = [];
      let col1 = [];
      let col2 = [];

      for (var i = 0; i < this.professors.length; i++){
        this.categories.add(this.professors[i]["Department"]);
      }

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

    // splitted pathways to alphabet categories, then splitted categories into 2 arrays, one array = one column
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
      for (var i = 0; i < alphabet.length; i++){
        var tmp = {
          "Category Name": alphabet[i],
          Professors: [],
        };
        for (var j = 0; j < this.professors.length; j++){
          var name = this.professors[j];
          var last_name = name.split(" ")[1];
          if (last_name.startsWith(alphabet[i])){
            tmp["Pathways"].push(this.professors[i]);
          }
        }
        tmp["Pathways"].sort(function(a,b){return a.split[" "][1] - b.split[" "][1]});

        // splitted categories into 2 arrays
        if (tmp["Pathways"].length > 0) {
          if (count < half_length) {
            col1.push(tmp);
            count += tmp["Pathways"].length + 0.2;
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

    // Go to the professor's page when clicked
    goPage(professor) {
      this.$router.push("/explore/" + professor);
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

.pathway-button {
  display: inline-block;
  background: white;
  border-style: none;
  text-align: justify;
  width: 95%;
}

.pathway-button:hover {
  background: rgba(108, 90, 90, 0.15) !important;
}

.courseInPath {
  cursor: pointer;
}

.courseInPath:hover {
  background-color: rgba(39, 130, 230, 0.5);
}
</style>
