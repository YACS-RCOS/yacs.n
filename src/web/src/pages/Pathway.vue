
<template>
  <b-container fluid>
    <b-button @click="listAlphabet()">List by Alphabet</b-button>
    <b-button @click="listCate()">List by Category</b-button>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="categories.length > 0" class="mx-auto w-75">
      
      <!-- pop-up window -->
      <b-modal ref="my-modal" >
        <div class="block text-left" v-if="showPath != null" md="10">
            <h3 class="text-center" style="color:#007bff">{{ showPath.Name[0] }}</h3>
            <br>
            <div v-for="(item, itemName) in showPath" :key="itemName">
                <h4 style="color:#3395ff">{{ itemName + ": " }}</h4>
                <li v-for="course in item" :key="course" v-on:click="goPage(course)" class="courseInPath">{{ course }}</li>
                <br>
            </div>
          </div>
      </b-modal>

      <b-row>
        <!-- splited categories into 2 arrays, so we can have 2 columns -->
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
                  <div v-for="pathway in categoryObj['Pathways']" :key="pathway['Name'][0]" role="tablist">
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

        <b-col
          v-for="(catCol, index) in categoryCols"
          :key="`catCol-${index}`"
          md="6"
          v-show="alphShow"
        >
        <p>Alphabet </p>
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
                  <div v-for="pathway in categoryObj['Pathways']" :key="pathway['Name'][0]" role="tablist">
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

    <b-row id = "Note" class="categoryBox">
      <b-col>
        <li>You can explore different pathway by clicking the pathway boxes. </li>
        <li>You can also check out the courses by clicking the listed courses. </li>
        <li>You will be directed to the department page if the course is not specified.</li>
        <li>However, the course may show up as "Course not found" if the course is not being offer this semester. </li>
      </b-col>
    </b-row>

  </b-container>
</template>



<script>
import json from './pathwayV2.json'
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  
  name: "Pathway",
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
          text: "Pathways"
        }
      ],
      categories: json,
      showPath: null,
      cateShow: true,
      alphShow : false
    };
    
  },
  computed:{
    // splited categories into 2 arrays, one array = one column
    categoryCols() {
      let ret = [];
      let col1 = [];
      let col2 = [];
      for (var i = 0; i < this.categories.length; i++) {
        if (i< this.categories.length/2) {
          col1.push(this.categories[i]);
        } else {
          col2.push(this.categories[i])
        }
      }
      ret.push(col1);
      ret.push(col2);
      return ret;
    }
  },
  methods: {

    listAlphabet(){
      this.cateShow = false;
      this.alphShow = true;
    },
    listCate(){
      this.cateShow = true;
      this.alphShow = false;
    },
    // Display a pop-up window when a pathway is clicked
    ShowPath(pathway){
        console.log(this.$refs["my-modal"]);
        console.log(pathway);
        this.showPath = pathway;
        this.$refs["my-modal"].show();
    },
    // Go to the course page when a course inside the pop-up window is clicked
    goPage(course){
        var subject = "" + course[0] + course[1] + course[2] + course[3];
        var courseID = "" + course[5] + course[6] + course[7] + course[8];
        if(course[4] != ' '){
            return;
        }
        if(course[8] == "X")
        {
            this.$router.push("/explore/" + subject);
        }
        else{
            this.$router.push("/explore/" + subject +"/" + subject + "-" + courseID);
        }
    }
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
  color:hsl(211,100%,60%);
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

.courseInPath{
    cursor: pointer;
}

.courseInPath:hover {
    background-color: rgba(39, 130, 230, 0.5);
}
</style>
