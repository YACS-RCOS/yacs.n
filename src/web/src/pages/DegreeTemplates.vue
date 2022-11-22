<script>
import degrees_json from "./DegreeTemplates.json";
import schools_json from "./schools.json";
export default {
  name: "DegreeTemplates",
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
      schools: schools_json,
      showPath: null,
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
      for(var i = 0; i < this.schools.length; i++){
        if (i < this.schools.length / 2) {
          col1.push(this.schools[i]);
        } else {
          col2.push(this.schools[i]);
        }
      }
      ret.push(col1);
      ret.push(col2);
      return ret;
    },
    categoryCols() {
      let ret = [];
      let col1 = [];
      let col2 = [];
      for (var i = 0; i < this.degrees.length; i++) {
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
    // splitted degrees to alphabet degrees, then splitted degrees into 2 arrays, one array = one column
    alphabetCols() {
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
      var half_length = Math.ceil(this.degrees.length / 2);
      var count = 0;
      // splitted degrees to alphabet degrees, then splitted degrees into 2 arrays
      for(var n = 0; n < alphabet.length; n++){ // iterates through each alphabet character and creates dictionary for each letter
        var tmp = {
          "Category Name":alphabet[n],
          Degrees:[],
        };
        for(var m = 0; m < this.degrees.length; m++){ // iterates through degrees
          if(this.degrees[m]["Major"].startsWith(alphabet[n])){
            // insert alphabetically within a letter category
            var index = 0;
            while(index < tmp["Degrees"].length){ // increment index until end of list or correct index is found 
              if(this.degrees[m]["Major"] < tmp["Degrees"][index]["Major"]){
                break;
              }
              index++;
            }
            tmp["Degrees"].splice(index, 0, this.degrees[m]); // insert degree into tmp's Degree's list at correct alphabetical location
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
    ShowPath(pathway) {
      console.log(this.$refs["my-modal"]);
      console.log(pathway);
      this.showPath = pathway;
      this.$refs["my-modal"].show();
    },
    // Go to the course page when a course inside the pop-up window is clicked
    goPage(course) {
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

.pathway-button {
  display: inline-block;
  background: blue;
  border-style: none;
  text-align: justify;
  width: 95%;
}

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