<template>
  <p>hi welcome to degree templates</p>
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
    getAverageForSem(creditsPerclass,gradeList) {
        //list of all credits in order of what they imputed
        //list of all grades in in order of inputed
        //will list gpa for the given semester
    },
    getTotalAvg(creditHours, GPA, creditsPerclass, gradeList){
        //number of credit hours
        //GPA from thoes credit hours
        //current semeser grade and creditsper class
        //will return what new gpa will be and how its affected
    }
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