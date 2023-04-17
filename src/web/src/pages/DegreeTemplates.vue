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
        List by School
      </b-button>
    </div>
    <div v-if="degrees.length > 0" class="mx-auto w-75">
      <b-modal ref="my-modal">
        <div class="block text-left" v-if="showMajor != null" md="40">
          <h3
            class="text-center"
            style="color: #007bff; margin-top: -5px; margin-bottom: 5px;"
          >
            {{ showMajor.Major }}
          </h3>
          <br />
            <div v-for="(item, itemName) in showMajor" :key="itemName">
              <h4 style="color: #3395ff; margin-top: -15px;">
                <div v-if="itemName === 'Y1'">
                  {{ "First Year: " }}
                </div>
                <div v-if="itemName === 'Y2'">
                  {{ "Second Year: " }}
                </div>
                <div v-if="itemName === 'Y3'">
                  {{ "Thind Year: " }}
                </div>
                <div v-if="itemName === 'Y4'">
                  {{ "Fourth Year: " }}
                </div>
              </h4>
              <div v-if="itemName != 'Major' && itemName != 'Y1' && itemName != 'Y2' && itemName != 'Y3'&& itemName != 'Y4'">
                <div
                  v-for="course in item" :key="course"
                >
                  <b v-if=" course === 'Fall' " style="color: #3395ff; margin-top: -20px;" >
                    {{ course }}
                  </b>
                  <b v-else-if=" course === 'Spring' " style="color: #3395ff; margin-top: -20px;">
                    {{ course }}
                  </b>
                  <b v-else-if=" course === 'The Arch Semester' " style="color: #3395ff; margin-top: -20px;">
                    {{ course }}
                  </b>
                  <!-- draggable class="list-group" :list="list1" group="people">
                    <b-button
                      @click="displayCourse(course)"
                      v-for="course in semester"
                      :key="course"
                    >{{ course.name }} | {{ course.creditHours }}</b-button>
                  </draggable> -->
                  <draggable class="list-group" :list="list1" group="people" v-else>
                    <b-button
                      @click="goPage(course)"
                      class="courseInPath">{{ course }}
                    </b-button>
                  </draggable>
                </div>
              </div>
            <br />
          </div>
        </div>
      </b-modal>
      <b-row>
        <b-col
          v-for="(school, index) in schoolCols"
          :key="`school-${index}`"
          md="6"
          v-show="cateShow"
        >
          <b-row
          v-for="schoolObj in school"
          :key="schoolObj['School Name'][0]"
          class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Category Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ schoolObj["School Name"][0] }}
                </h3>
              </b-row>
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the Pathway Categories list -->
                  <div
                    v-for="major in schoolObj['Majors']"
                    :key="major['Major']"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <b-button
                          @click="ShowMajor(major)"
                          squared
                          variant="light"
                          class="pathway-button m-0 ml-1"
                        >
                      {{ major['Major'] }}
                    </b-button>
                    </div>
                  </div>
                </div>
              </b-row>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
      <b-row>
        <b-col
          v-for="(school, index) in alphabetCols"
          :key="`school-${index}`"
          md="6"
          v-show="alphShow"
        >
          <b-row
          v-for="schoolObj in school"
          :key="schoolObj['Category Name']"
          class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Category Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ schoolObj["Category Name"] }}
                </h3>
              </b-row>
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the Pathway Categories list -->
                  <div
                    v-for="major in schoolObj['Degrees']"
                    :key="major['Major']"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <b-button
                          @dblclick="ShowMajor(major)"
                          squared
                          variant="light"
                          class="pathway-button m-0 ml-1"
                        >
                        {{ major['Major'] }}
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
      loadingMessage="DegreeTemplates"
      :topSpacing="30"
    />
  </b-container>
</template>

<script>
import degrees_json from "./DegreeTemplates.json";
import CenterSpinnerComponent from "../components/CenterSpinner";
import draggable from "vuedraggable";

export default {
  name: "DegreeTemplates",
  components: {
    draggable,
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
          text: "DegreeTemplates",
        },
      ],
      degrees: degrees_json,
      showMajor: null,
      cateShow: true,
      alphShow: false,
    };
  },
  computed: {
    /*
      For categoryCols, we probably want to get some sort of dictionary containing each of the
      Schools that contain majors and sort the displaying in this function.    
    */
    // splitted degrees into 2 arrays, one array = one column
    schoolCols(){
      let ret = [];
      let col1 = [];
      let col2 = [];
      for(var i = 0; i < this.degrees.length; i++){
        if (i < this.degrees.length / 2) {
          col1.push(this.degrees[i]);
        } else {
          col2.push(this.degrees[i]);
        }
      }
      ret.push(col1);
      ret.push(col2);
      return ret;
    },
    // split degrees to alphabet degrees, then splitted degrees into 2 arrays, one array = one column
    alphabetCols() {
      let alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
      let ret = [];
      let col1 = [];
      let col2 = [];

      var degreeCount = 0;
      for(var m = 0; m < this.degrees.length; m++){
        degreeCount += this.degrees[m]['Majors'].length;
      }

      var half_length = Math.ceil(degreeCount / 2);
      var count = 0;
      // split degrees to alphabet degrees, then split degrees into 2 arrays
      for(var n = 0; n < alphabet.length; n++){ // iterates through each alphabet character and creates dictionary for each letter
        var tmp = {
          "Category Name":alphabet[n],
          Degrees:[],
        };

        for(var i = 0; i < this.degrees.length; i++){
          for(var j = 0; j < this.degrees[i]['Majors'].length; j++){
            var bool = 0;
            for(var k = 0; k < tmp['Degrees'].length; k++){
              if(tmp['Degrees'][k]['Major'] === this.degrees[i]['Majors'][j]['Major']){
                bool = 1;
              }
            }
            if(bool === 1){
              break;
            }
            if(this.degrees[i]['Majors'][j]['Major'].startsWith(alphabet[n])){
              var index = 0;
              while(index < tmp["Degrees"].length){
                if(this.degrees[i]['Majors'][j]['Major'] < tmp["Degrees"][index]["Major"]){
                  break;
                }
                index++;
              }
              tmp["Degrees"].splice(index, 0, this.degrees[i]['Majors'][j]);
            }
          }
        }

        if (tmp["Degrees"].length > 0){
          if(count < half_length){
            col1.push(tmp);
            count += tmp["Degrees"].length + 0.2;
          } else{
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
    // Display a pop-up window when a pathway is clicked
    ShowMajor(major) {
      console.log(this.$refs["my-modal"]);
      console.log(major);
      this.showMajor = major;
      this.$refs["my-modal"].show();
    },
    // Go to the course page when a course inside the pop-up window is clicked
    printCourse(course){
      course;
    },
    
    goPage(course) {

      let c_lower = course.toLowerCase();
      if (c_lower.includes("math elective") || c_lower.includes("math option") || c_lower.includes("mathematics")){
        console.log("MATH elective");
        this.$router.push("/explore/MATH");
        return;
      }      

      if (c_lower.includes("option") || c_lower.includes("elective")){
        console.log("other elective");
        this.$router.push("/explore/");
        return;
      }

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