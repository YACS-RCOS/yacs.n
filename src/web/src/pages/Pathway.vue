
<template id = "body">
  <div fluid class="py-3 h-100">
    <h1>Intergrated Pathways</h1>
    <br>

    <b-modal ref="my-modal" >
      <div class="block text-left" v-if="showPath != null" md="10">
        <h3 class="text-center" style="color:#007bff">{{ showPath.Name[0] }}</h3>
        <br>
        <div v-for="(item, category) in showPath" :key="category"> 
            <h4 style="color:#3395ff">{{ category + ": " }}</h4>
            <li v-for="course in item" :key="course" v-on:click="goPage(course)" class="courseInPath">{{ course }}</li>
            <br>
        </div>
      </div>
    </b-modal>

    <b-row id = "items">
      <b-col class = "pathBox" md="3" sm="4" v-for="pathway in pathways" :key="pathway['Name'][0]" v-on:click="ShowPath(pathway)">
        <div calss = "roundBox ">
            <p class = "pathwayName text-center" > {{ pathway["Name"][0] }}</p>
        </div>
      </b-col>
    </b-row>

    <b-row id = "Note">
        <b-col>
            <li>You can explore different pathway by clicking the pathway boxes. </li>
            <li>You can also check out the courses by clicking the listed courses. </li>
            <li>You will be directed to the department page if the course is not specified.</li>
            <li>However, the course may show up as "Course not found" if the course is not being offer this semester. </li>
        </b-col>
    </b-row>
  </div>
</template>

<script>
import json from './pathway.json'
export default {
  name: "Pathway",
  showPath: null,
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

    data(){
        return{
            pathways: json,
            showPath: null
        }
    },
};
</script>

<style>
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
