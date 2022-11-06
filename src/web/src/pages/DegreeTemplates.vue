<template>
<<<<<<< Updated upstream
  <p>hi welcome to degree templates</p>
</template>

<script>
export default {
  name: "DegreeTemplates",
};
</script>

<style></style>
=======
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
      <div class="majorsBox">
        <ul>
          <li v-for="major in majors" :key="major.Major">
            {{ major.Major }}
          </li>
        </ul>
      </div>
  </b-container>
</template>

<script>
import json from "./DegreeTemplates.json";

export default {
  name: "Degree Templates",
  data() {
    return {
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Degree Templates",
        },
      ],
      majors: json,
      showPath: null,
      cateShow: true,
      alphShow: false,
    };
  },
  computed: {
    // splitted categories into 2 arrays, one array = one column
    categoryCols() {
      let ret = [];
      let col1 = [];
      let col2 = [];
      for (var i = 0; i < this.categories.length; i++) {
        if (i < this.categories.length / 2) {
          col1.push(this.categories[i]);
        } else {
          col2.push(this.categories[i]);
        }
      }
      ret.push(col1);
      ret.push(col2);
      return ret;
    },

    // splitted pathways to alphabet categories, then splitted categories into 2 arrays, one array = one column
    alphabetCols() {
      let cols = [];
      // put all pathways in one array
      for (var i = 0; i < this.categories.length; i++) {
        for (var j = 0; j < this.categories[i]["Pathways"].length; j++) {
          cols.push(this.categories[i]["Pathways"][j]);
        }
      }

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
      var half_length = Math.ceil(cols.length / 2);
      var count = 0;
      // splitted pathways to alphabet categories, then splitted categories into 2 arrays
      for (var n = 0; n < alphabet.length; n++) {
        var tmp = {
          "Category Name": alphabet[n],
          Pathways: [],
        };
        for (var m = 0; m < cols.length; m++) {
          if (cols[m]["Name"][0].startsWith(alphabet[n])) {
            var index = 0;
            while (index < tmp["Pathways"].length) {
              if (cols[m]["Name"][0] < tmp["Pathways"][index]["Name"][0]) {
                break;
              }
              index++;
            }
            tmp["Pathways"].splice(index, 0, cols[m]);
          }
        }
        // splitted categories into 2 arrays
        if (tmp["Pathways"].length > 0) {
          if (count < half_length) {
            col1.push(tmp);
            count += tmp["Pathways"].length + 0.2;
          } else {
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
.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}
.majorsBox {
    display: flex;
    align-items: center;
    justify-content: center;
    color: hsl(211, 100%, 60%);
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

>>>>>>> Stashed changes
