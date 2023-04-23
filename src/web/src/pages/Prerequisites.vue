
<template>
  <b-container fluid>
    <div v-if="errorM" class ="misread">{{ errorM }}</div>
    <header style = "color:deepskyblue;">
      <h2>Enter Prerequisite Course Code</h2>
    </header>
    
    <!-- <label for="department">Class code</label> -->

    <v-select
    v-model = "deptCode" :items="deptL" label="select department code"></v-select>
    <!-- <input id = "department" v-model="department" placeholder="ex.CSCI" type="text" maxlength="4"/> -->

    <!-- bug with length of number -->
    <input v-model="courseID" placeholder="course number" type="number" max="9999"/>
    
    <button class = "editedButton" @click = "addCourse">Submit</button>
    


    <button class = "editedButton" @click = "removePrereq">Undo</button>
    <button class = "editedButton" @click = "clearing">Erase</button>
    
    <span class = "info">Click on any prerequisite to delete them</span>
    
    <ul>
      <li v-for="(course, index) in Plist" :key="index" v-on:click = "deleteCourse(index)">{{ course }}</li>
    </ul>
  </b-container>
</template>

<script>
// import components from "@components/DepartmentList"; 


export default {
  data() {
    const Plist = localStorage.getItem('Plist');
    
    if (Plist) {
        this.Plist = Plist.split(",");
      } else {
        this.Plist = [];
      }
      
    return {
      combination: '',
      department: '',
      errorM: '',
      courseID: null,
      this:Plist,
      deptL:['ARTS', 'COGS', 'STSH', 'STSS', 'COMM', 'ECON', 'GSAS', 'IHSS', 'LANG', 'LITR', 
      'PHIL', 'PSYC', 'WRIT', 'BMED', 'CHME', 'ECSE', 'ENVE', 'MANE', 'MTLE', 'CIVL', 'ENGR', 
      'ISYE', 'EPOW', 'BCBP', 'CSCI', 'ERTH', 'IENV', 'ISCI', 'MATP', 'PHYS', 'ASTR', 'BIOL', 'CHEM', 
      'MATH', 'ITWS', 'ARCH', 'LGHT', 'MGMT', 'ADMN', 'USAF', 'USNA', 'USAR'],
      deptcode:null,

    };
  },
  methods: {
    addCourse() {
      if (this.courseID.trim() !== '' && this.department.trim() !== '') {
        this.department = this.department.toUpperCase();
        if(this.courseID > 9999 || this.courseID < 1000) {
         this.errorM = "invalid course number, change course ID number"
         setTimeout(() => {
          this.errorM = ''
         }, 2000)

        } else {
          this.combination  = this.department + "-" + this.courseID;
          this.Plist.push(this.combination);
          this.courseID = '';
          this.department = '';
        }
        
      }
    },
    removePrereq(){
      
      this.Plist.pop();
      this.courseID = '';
      this.department = 'x';
      this.department = '';
      
    },
    deleteCourse(index) {
      // if(this.courseID.trim() == '' || this.department.trim() == ''){
        this.combination = this.Plist[index];
        this.Plist.splice(index,1);
        this.courseID = '';
        this.department = 'x';
        this.department = '';
      // }
      
    },
    clearing() {
      this.Plist = [];
      this.courseID = '';
      this.department = 'x';
      this.department = '';
    }
  },
  watch: {
    Plist: {
      handler() {
        localStorage.setItem('Plist', this.Plist.join(','));
      },
      deep: true,
    },
  },
};
</script>

<style>
input {
  margin-left: 10px;
  margin-right: 10px;
}

.info {
  display: block;
}
.editedButton {
  background-color: #b5b3e2;
  border: none;
  text-align: center;
  margin-left: 30px;
  margin-right: 10px;
  border-radius: 8px;
}

.courseButton {
  background-color: #3f35eb;
  border: none;
  text-align: center;
  margin-left: 30px;
  margin-right: 10px;
  border-radius: 8px;
}

.misread {
  background-color: red;
  color: white;
  padding: 10px;
}
</style>