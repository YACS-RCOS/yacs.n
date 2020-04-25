<template>
  <div id='footer'>
    <hr />
    <section id='main-block'>
      <b-container>
        <b-row>
          <b-col/>
          <b-col>
            <!-- TODO: Autogenerate these when doing the user side, semester select -->
            <strong class="section-head">Other Semesters</strong>
            <p class="disabled"> {{semester}} </p>
            <a
              v-for="option of otherSemesters"
              :key="option.text"
              class="semester"
              :disabled="option.text === semester"
              @click="updateCurrentSemester(option.text)"
            >
              {{option.value}}
            </a>
          </b-col>

          <b-col>
            <strong class="section-head">Contact Us</strong>
            <a class="link" href="https://github.com/YACS-RCOS/yacs.n"  target="_blank" >Contribute (GitHub)</a>
            <a class="link" href="https://github.com/YACS-RCOS/yacs.n/issues/new?assignees=&labels=Feature+Request&template=feature-request.md&title=Feature+Request+—+Make+YACS+Great" target="_blank" >Request a Feature</a>
            <a class="link" href= "https://github.com/YACS-RCOS/yacs.n/issues/new?assignees=&labels=bug&template=bug_report.md&title=Bug+—+Someone+made+an+oopsie" target="_blank" >Report a Bug</a>
          </b-col>

          <b-col>
            <strong class="section-head">Legal Stuff</strong>
            <a class="link" href="http://opensource-template.wikidot.com/legal:terms-of-use" target="_blank">Terms of Use</a>
            <!-- <a class="link" href=#>Cookies</a> -->
          </b-col>
          <b-col/>
        </b-row>
      </b-container>
    </section>
    <!-- <hr> -->
    <section id='credits'>
      <p class='text-center'>Built by YACS under RCOS at RPI</p>
    </section>

  </div>
</template>

<script>

import { getSemesters } from '@/services/YacsService';

export default {
    name: 'Footer',
    props: {
      semester: String
    },
    data() {
      return {
        semesterOptions: []
      }
    },
    methods: {
      updateCurrentSemester(to) {
        console.log("in change emit of footer");
        this.$emit("changeCurrentSemester", to);
      }
    },
    computed: {
      otherSemesters: function(){
        var semesters = [];
        for(var sem of this.semesterOptions){
          if(sem.text != this.semester){
            semesters.push(sem);
          }
        }
        return semesters
      }
    },
    created () {
      getSemesters().then(data  => {
        this.semesterOptions.push(...data.map(s => ({text: s.semester, value: s.semester})));
      });
    }
}
</script>

<style scoped lang="scss">

#footer {
  width: 100%;
  #main-block {
    background: white;
    color: black;
    padding-top: 25px;
    width: 100%;
    height: auto;
    margin: 0px !important;

    strong.section-head {
      color: #3D4959;
      margin-bottom: 2px;
    }

    a.semester {
      color: inherit;
      display: table;
      font-weight: bold;
      font-size:16px;
      cursor:pointer;
      width:auto;
    }

    a.semester:hover{
      text-decoration: underline;
    }

    p.disabled {
      color: inherit;
      display: block;
      font-size:16px;
      margin: 0;
    }

    a.link {
      color: inherit;
      display: table;
    }

    a.link#current {
      color: grey;
    }

    button:disabled {
      cursor: inherit;
    }

  }

  #credits {
    /* background: #3D4959; */
    width: 100%;
    height: auto;
    padding: 0px;
    margin: 0px;
    margin-top: 10px;
    padding: 10px 0px;
    font-size: 15px;

    p {
      color: #3D4959;
      margin: 0;
      margin-left: -30px;
    }
  }

}

</style>
