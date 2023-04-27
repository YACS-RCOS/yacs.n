<!-- 

Dev Documentation:
  
  Current Issues:
    - Drag and Drop Bug: When dragging a and letting go while hovering over another course,
      hovering over the courses are grouped together and both pop up when hovered over.
    - Scrolling Bug: When dragging a course to the boundary of the browser, the background
      page scrolls up and down before the modal that the template is inside of.
      - Potential fix: have a redirect to a page rather than a modal similar to ExplorePage
        with its different departments.

  Prospective Features:
    - Create a database connection to the YACS database and pull data from there
    - Add a "+" button to add a course to a template
    - Right click menu:
      - Add a "Remove" button to remove a course from a template
      - Add a "Move" button to move a course to a different semester
    - Exportability of the template to a PDF or a CSV
    - Add a "Save" button to save the template to the database/locally
    - Add a "Load" button to load a template from the database/locally
    - Course Conflict Detection (if a course is already in the template, it should be highlighted)
-->

<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

    <!-- buttons to switch between alphabet order and category order -->
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

    <!-- Course Template Modal -->
    <div v-if="degrees.length > 0" class="mx-auto w-100">
      <b-modal ref="my-modal" size="xl">
        <div class="block text-left" v-if="showMajor != null" b-md="90">
          <h2
            class="text-center"
            style="color: #007bff; margin-top: -5px; margin-bottom: 5px;"
          >
            {{ showMajor.Major }}
          </h2>

          <!-- Draggable dispenser and trash can -->
          <b-row>
            <b-col>
              <b-button 
                @click="addNewItem()"
                style="background-color: #8ab4f8; color: white; border-radius: 3px; border-color: #f0e4e4; margin-top: 2px"
              >
                Add new item
              </b-button>
              <b-row v-for="draggable_item in draggables_list" :key="draggable_item">
                <draggable v-modal="semester" class="list-group" :list="list1" group="people" :options="{ preventOnFilter: true }">
                  <b-button
                    @click="goPage(draggable_item)"
                    style="background-color: #8ab4f8; color: white; border-radius: 3px; border-color: #f0e4e4; margin-top: 2px"
                    class="courseInTemplate">
                      {{ draggable_item }}  
                  </b-button>
                </draggable>
              </b-row>
            </b-col>
            <b-col>
              <b-button
                @click="trash()"
                style="background-color: #8ab4f8; color: white; border-radius: 3px; border-color: #f0e4e4; margin-top: 2px"
                class="courseInTemplate"
              >
                Trash
              </b-button>
            </b-col>
          </b-row>

          <div v-for="(item, itemName) in showMajor" :key="itemName">
            <div v-if="itemName === 'Y1'"> <!-- Year 1 -->
              <h4 style="color: #3395ff; margin-top: -10px;">
                {{ "First Year: " }}
              </h4>
              <b-row>
                <b-col v-for="semester in [showMajor.Y1S1, showMajor.Y1S2]" :key="semester">
                  <div v-for="course in semester" :key="course">
                    <b v-if=" course === 'Fall' " style="color: #3395ff; margin-top: -20px;" >
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'Spring' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'The Arch Semester' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <draggable v-modal="semester" class="list-group" :list="list1" group="people" :options="{preventOnFilter: true}" v-else>
                      <b-button
                        @click="goPage(course)"
                        style="background-color: #8ab4f8; color: white; border-radius: 3px; border-color: #f0e4e4; margin-top: 2px"
                        class="courseInTemplate">{{ course }}
                        <!-- Create a right click action here for a menu display for each course -->
                      </b-button>
                    </draggable>
                  </div>
                </b-col>
              </b-row>
            </div>
            <div v-else-if="itemName === 'Y2'"> <!-- Year 2 -->
              <h4 style="color: #3395ff; margin-top: -25px;">
                {{ "Second Year: " }}
              </h4>
              <b-row>
                <b-col v-for="semester in [showMajor.Y2S1, showMajor.Y2S2]" :key="semester">
                  <div v-for="course in semester" :key="course">
                    <b v-if=" course === 'Fall' " style="color: #3395ff; margin-top: -20px;" >
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'Spring' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'The Arch Semester' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <draggable class="list-group" :list="list1" group="people" v-else >
                      <b-button
                        @click="goPage(course)"
                        style="background-color: #8ab4f8; color: white; border-radius: 3px; border-color: #f0e4e4; margin-top: 2px"
                        class="courseInTemplate">{{ course }}
                      </b-button>
                    </draggable>
                  </div>
                </b-col>
              </b-row>
            </div>
            <div v-else-if="itemName === 'Y3'"><!-- Year 3 -->
              <h4 style="color: #3395ff; margin-top: -25px;">
                {{ "Third Year: " }}
              </h4>
              <b-row>
                <b-col v-for="semester in [showMajor.Y3S1, showMajor.Y3S2]" :key="semester">
                  <div v-for="course in semester" :key="course">
                    <b v-if=" course === 'Fall' " style="color: #3395ff; margin-top: -20px;" >
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'Spring' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'The Arch Semester' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <draggable class="list-group" :list="list1" group="people" v-else >
                      <b-button
                        @click="goPage(course)"
                        style="background-color: #8ab4f8; color: white; border-radius: 3px; border-color: #f0e4e4; margin-top: 2px"
                        class="courseInTemplate">{{ course }}
                      </b-button>
                    </draggable>
                  </div>
                </b-col>
              </b-row>
            </div>
            <div v-else-if="itemName === 'Y4'"> <!-- Year 4 -->
              <h4 style="color: #3395ff; margin-top: -25px;">
                {{ "Fourth Year: " }}
              </h4>
              <b-row>
                <b-col v-for="semester in [showMajor.Y4S1, showMajor.Y4S2]" :key="semester">
                  <div v-for="course in semester" :key="course">
                    <b v-if=" course === 'Fall' " style="color: #3395ff; margin-top: -20px;" >
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'Spring' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'The Arch Semester' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <draggable class="list-group" :list="list1" group="people" v-else >
                      <b-button
                        @click="goPage(course)"
                        style="background-color: #8ab4f8; color: white; border-radius: 3px; border-color: #f0e4e4; margin-top: 2px"
                        class="courseInTemplate">{{ course }}
                      </b-button>
                    </draggable>
                  </div>
                </b-col>
              </b-row>
            </div>
            <div v-else-if="itemName === 'Y5'"> <!-- Year 5 -->
              <h4 style="color: #3395ff; margin-top: -25px;">
                {{ "Fifth Year: " }}
              </h4>
              <b-row>
                <b-col v-for="semester in [showMajor.Y5S1, showMajor.Y5S2]" :key="semester">
                  <div v-for="course in semester" :key="course">
                    <b v-if=" course === 'Fall' " style="color: #3395ff; margin-top: -20px;" >
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'Spring' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <b v-else-if=" course === 'The Arch Semester' " style="color: #3395ff; margin-top: -20px;">
                      {{ course }}
                    </b>
                    <draggable class="list-group" :list="list1" group="people" v-else >
                      <b-button
                        @click="goPage(course)"
                        style="background-color: #8ab4f8; color: white; border-radius: 3px; border-color: #f0e4e4; margin-top: 2px"
                        class="courseInTemplate">{{ course }}
                      </b-button>
                    </draggable>
                  </div>
                </b-col>
              </b-row>
            </div>
            <br/>
          </div>
        </div>
      </b-modal>

      <!-- Majors Ordered by their Department -->
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
                  <!-- LOOP Through the RPI schools -->
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
                          class="template-button m-0 ml-1"
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

      <!-- Majors Ordered Alphabetically -->
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
                  <!-- LOOP Through the template Categories list -->
                  <div
                    v-for="major in schoolObj['Degrees']"
                    :key="major['Major']"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <b-button
                          @click="ShowMajor(major)"
                          squared
                          variant="light"
                          class="template-button m-0 ml-1"
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
// import templateMenu from "../components/TemplateMenu.vue";
import draggable from "vuedraggable";

export default {
  name: "DegreeTemplates",
  components: {
    draggable,
    // templateMenu: templateMenu,
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
      templateModalClass: "template-modal-class",
    };
  },
  computed: {

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

    alphabetCols() {
      let alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
      let page_columns = [];
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

        // iterates through each degree and adds it to the dictionary if it starts with the current alphabet character
        for(var i = 0; i < this.degrees.length; i++){
          for(var j = 0; j < this.degrees[i]['Majors'].length; j++){
            var bool = 0;

            // checks if the degree is already in the dictionary
            for(var k = 0; k < tmp['Degrees'].length; k++){
              if(tmp['Degrees'][k]['Major'] === this.degrees[i]['Majors'][j]['Major']){
                bool = 1;
              }
            }
            if(bool === 1){
              break;
            }

            // adds the degree to the dictionary if it starts with the current alphabet character
            if(this.degrees[i]['Majors'][j]['Major'].startsWith(alphabet[n])){
              var index = 0;

              // finds the index to insert the degree at
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

        // adds the dictionary to the column arrays
        if (tmp["Degrees"].length > 0){
          if(count < half_length){
            col1.push(tmp);
            count += tmp["Degrees"].length + 0.2;
          } else{
            col2.push(tmp);
          }
        }
      }

      page_columns.push(col1);
      page_columns.push(col2);
      return page_columns;
    },
  },

  update:{
    addNewItem() {
      this.draggables_list.push({ name: 'New Item' });
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

    ShowMajor(major) {
      console.log(this.$refs["my-modal"]);
      console.log(major);
      this.showMajor = major;
      this.$refs["my-modal"].show();
    },

    printCourse(course){
      course;
    },
    
    goPage(course) {

      if(course.length < 4){
        return;
      }

      var subject = "" + course[0] + course[1] + course[2] + course[3];

      /* Elective handling:
      Would be better if this wasn't hard coded, but there's no mapping of keywords to subjects (wip?)
      */
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

.template-modal-class {
  background-color: rgb(32,28,36);
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto;
}

.template-button {
  display: inline-block;
  background: white;
  border-style: none;
  text-align: justify;
  width: 95%;
}

.template-button:hover {
  background: rgba(108, 90, 90, 0.15) !important;
}

.list-group:hover{
  transform: scale(1.05);
  box-shadow: 3px 3px 3px #c2c4c8;
  z-index: 999;
}

.courseInTemplate {
  cursor: pointer;
  background-color: rgba(4, 68, 135, 0.2);
  
}

.courseInTemplate:hover {
  background-color: rgba(39, 130, 230, 0.5);
  border-radius: 3px;
  border-color: #f0e4e4;
  margin-top: 2px
}

</style>