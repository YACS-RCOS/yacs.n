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
        @click="listCat()"
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

    <div v-if="professors.length > 0" class="mx-auto w-75">
      <b-row>
        

        <!-- splitted Pathways in alphabet order -->
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
                  <!-- LOOP Through the Pathway Alphabet list -->
                  <div
                    v-for="prof in alphabetObj['Professors']"
                    :key="prof['Name']"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <!-- pathway button -->
                      <b-button
                        @click="ShowProf(prof)"
                        squared
                        variant="light"
                        class="pathway-button m-0 ml-1"
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
      catShow: false,
      alphShow: true,
    };
  },
  computed: {
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
          "Letter": alphabet[i],
          "Professors": [],
        };
        for (var j = 0; j < this.professors.length; j++){
          var name = this.professors[j]["Name"];
          var last_name = name.split(" ")[1];
          if (last_name.startsWith(alphabet[i])){
            var index = 0;
            while (index < tmp["Professors"].length){
              if (last_name < tmp["Professors"][index]["Name"].split(" ")[1]){
                break
              }
              index++;
            }
            tmp["Professors"].splice(index, 0, this.professors[j]);
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
      this.catShow = false;
      this.alphShow = true;
    },
    listCat() {
      this.catShow = true;
      this.alphShow = false;
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
