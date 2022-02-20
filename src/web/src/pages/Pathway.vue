
<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="pathways.length > 0" class="mx-auto w-75">
      <b-row>
        <!-- 2 arrays in schoolDepartmentObjects, so 2 columns -->
        <b-col
          v-for="(deptCol, index) in schoolDepartmentObjects"
          :key="`deptCol-${index}`"
          md="6"
        >
          <b-row
            v-for="deptObj in deptCol"
            :key="deptObj.school"
            class="departmentBox border m-2 mb-4"
          >
            <b-col>
              <!-- Category Title  -->
              <b-row class="school-name">
                <h3 class="m-1 ml-2">
                  {{ deptObj.school }}
                </h3>
              </b-row>
              <!-- Pathway Title  -->
              <b-row>
                <PathwayCategoriesList
                  :categories="deptObj.departments"
                  :deptClassDict="deptClassDict"
                  v-on:showCourseInfo="showCourseInfo($event)"
                ></PathwayCategoriesList>
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
      loadingMessage="Departments"
      :topSpacing="30"
    />
  </b-container>
</template>



<script>
import json from './pathway.json'
import { mapGetters, mapState } from "vuex";
import { COURSES } from "@/store";
import PathwayCategoriesListComponenet from "@/components/PathwayCategoriesList";
import { generateRequirementsText } from "@/utils";
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  name: "Pathway",
  components: {
    PathwayCategoriesList: PathwayCategoriesListComponenet,
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
      // hardcoding all categories, please replace with data imported from json files when it is available
      categories: ["Arts/Designs", "Cognitive Science", "Communication/Writing", "Ecology", "Economics", 
                   "Information Technology", "Language", "Media/Music", "Philosophy", "Social Science", "Transfer Student"],
      showPath: null
    };
  },
  methods: {
    ShowPath(pathway){
        //console.log(pathway);
        this.showPath = pathway;
        this.$refs["my-modal"].show();
    },
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

.departmentBox {
  text-align: center;
}

.school-name {
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}

body {
  text-align: center;
}

#items{
    font-size: 20px;
}

.pathBox{
    cursor: pointer;
    border-radius: 2%;
    margin: 0;
}

.roundBox{
    cursor: pointer;
    border-radius: 2%;
    margin: 0;
}
.pathwayName{
    background-color: rgba(39, 130, 230, 0.5);
    height: 100px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 2%;
}

.pathwayName:hover {
    background-color: rgba(39, 130, 230, 1);
}

.courseInPath{
    cursor: pointer;
}

.courseInPath:hover {
    background-color: rgba(39, 130, 230, 0.5);
}

.marked{
  border-color: black;
  border: 1ch;
}

</style>
