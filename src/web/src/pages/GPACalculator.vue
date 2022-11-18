<template>
  <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
            <b-tab class="flex-grow-1" data-cy="course-search-tab">
              <template v-slot:title>
                <div class="text-center" data-cy="course-search-tab-header">   
                  GPA calculator for semester               
                </div>
              </template>
              <b-card-text class="w-100 d-flex flex-grow-1 flex-column">

                <label for="usr">Name:</label>
                <input type="text" class="form-control">


                <input v-model="classes" placeholder="Number of classes this semester">
                <p>Number of Classes: {{ classes }}</p>

                




              </b-card-text>
            </b-tab>

            <b-tab class="flex-grow-1" data-cy="selected-courses-tab">
              <template v-slot:title>
                <div class="text-center" data-cy="selected-courses-tab-header">
                  GPA calculator for total time  
                </div>
              </template>
              <b-card-text class="w-100 d-flex flex-grow-1 flex-column">



                <p>Enter GPA and number of Credits</p>




              </b-card-text>
            </b-tab>
   </b-tabs>
</template>
  
<script>
export default {
  name: "GPACalculator",
  data() {
    return {
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "GPACalculator",
        },
      ],
    };
  },
  computed: {
    //getAverageForSem(creditsPerclass,gradeList) {
        //list of all credits in order of what they imputed
        //list of all grades in in order of inputed
        //will list gpa for the given semester
        
    //},
    //getTotalAvg(creditHours, GPA, creditsPerclass, gradeList){
        //number of credit hours
        //GPA from thoes credit hours
        //current semeser grade and creditsper class
        //will return what new gpa will be and how its affected
    //}
  }
};
</script>

<style>
.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}
</style>