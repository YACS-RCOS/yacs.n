<template>
  <div class="d-flex flex-column flex-grow-1">
    <!-- LOOP Through the Pathway Categories list -->
    <div v-for="pathway in pathways" :key="pathway['Name'][0]" role="tablist">
      <template>

        <!-- pop-up window -->
        <div class="mt-1 mb-1 w-100">
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
      </template>
    </div>
  </div>
</template>

<script>
import "@/typedef";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";

export default {
  name: "PathwayCategoriesList",
  components: {},
  data() {
    return {
      faInfoCircle,
      showPath: null,
    };
  },
  props: {
    pathways: Array,
  },
  methods: {
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

<style scoped lang="scss">
.pathway-button {
  display: inline-block;
  background: white;
  border-style: none;
  text-align: justify;
  width: 95%;
}

.pathway-button:hover {
  //important because when you click the color changes and thats annoying
  background: rgba(108, 90, 90, 0.15) !important;
}
</style>
