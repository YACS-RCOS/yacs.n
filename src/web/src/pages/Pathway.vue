
<template id = "body">
  <div fluid class="py-3 h-100">
    <h1>Intergrated Pathways</h1>

    <b-modal ref="my-modal" >
      <div class="block text-left" v-if="showPath != null" md="10">
        <h3 class="text-center" style="color:#d6001c">{{ showPath.Name[0] }}</h3>
        <div v-for="(item, category) in showPath" :key="category"> 
            <h4 style="color:#c35442">{{ category + ": " }}</h4>
            <li v-for="course in item" :key="course" v-on:click="goPage(course)">{{ course }}</li>
            <br>
        </div>
      </div>
    </b-modal>

    <b-row>
      <b-col class = "pathBox" md="4" v-for="pathway in pathways" :key="pathway['Name']" v-on:click="ShowPath(pathway)">
        <div calss = "roundBox">
            <p class = "pathwayName text-center" > {{ pathway["Name"][0] }}</p>
           
        </div>
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
        this.$router.push("/explore/" + subject +"/" + subject + "-" + courseID)
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
.draggable-placeholder-inner {
  border: 1px dashed #0088f8;
  box-sizing: border-box;
  background: red;
  color: red;
  text-align: center;
  padding: 10px;
  display: flex;
  align-items: center;
}

.pathwayName{
    background: #ab2328;
    height: 45px;
}

</style>
