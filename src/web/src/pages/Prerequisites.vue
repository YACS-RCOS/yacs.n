
<template>
  <div>
    <header style = "color:deepskyblue;">
      <h2>Enter Prerequisite Course Code</h2>
    </header>
    
    <label for="department">Department code</label>
    <input id = "department" v-model="department" type="text" maxlength="4"/>

    <!-- bug with length of number -->
    <input v-model="courseID" type="number" max="9999"/>
    
    <button @click = "addCourse">Submit</button>
    <button @click = "removePrereq">Undo</button>
    <span class = "info">Click on any prerequisite to delete them</span>
    
    <ul>
      <li v-for="(course, index) in Plist" :key="index" v-on:click = "deleteCourse(index)">{{ course }}</li>
    </ul>
  </div>
</template>

<script>


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
      courseID: null,
      this:Plist,
    };
  },
  methods: {
    addCourse() {
      if (this.courseID.trim() !== '' && this.department.trim() !== '') {
        this.department = this.department.toUpperCase();
        if(this.courseID > 9999) {
          const temper = this.courseID.toString().splice(0,4);
          this.courseID = parseInt(temper);
        }
        this.combination  = this.department + "-" + this.courseID;
        this.Plist.push(this.combination);
        this.courseID = '';
        this.department = '';
      }
    },
    removePrereq(){
      
      this.Plist.pop();
      this.courseID = '';
      this.department = 'x';
      this.department = '';
      
    },
    deleteCourse(index) {
      if(this.courseID.trim() == '' || this.department.trim() == ''){
        this.combination = this.Plist[index];
        this.Plist.splice(index,1);
        this.courseID = '';
        this.department = 'x';
        this.department = '';
      }
      
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
button {
  margin-left: 30px;
  margin-right: 10px;
}
.info {
  display: block;
}

</style>