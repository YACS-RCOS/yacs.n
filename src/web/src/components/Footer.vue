<template>
  <div id="footer">
    <section id="main-block">
      <b-container>
        <b-row cols="2" cols-md="3" align-h="center">
          <b-col class="link-group">
            <strong class="section-head">Other Semesters</strong>
            <a
              v-for="option of otherSemesters"
              :key="option.text"
              class="link"
              :disabled="option.text === selectedSemester"
              @click="updateSelectedSemester(option.text)"
            >
              {{ option.value }}
            </a>
          </b-col>

          <b-col class="link-group">
            <strong class="section-head">Contact Us</strong>
            <a
              class="link"
              href="https://github.com/YACS-RCOS/yacs.n"
              target="_blank"
              rel="noopener"
            >
              Contribute (GitHub)
            </a>
            <a
              class="link"
              href="https://github.com/YACS-RCOS/yacs.n/issues/new?assignees=&labels=Feature+Request&template=feature-request.md&title=Feature+Request+—+Make+YACS+Great"
              target="_blank"
              rel="noopener"
            >
              Request a Feature
            </a>
            <a
              class="link"
              href="https://github.com/YACS-RCOS/yacs.n/issues/new?assignees=&labels=bug&template=bug_report.md&title=Bug+—+Someone+made+an+oopsie"
              target="_blank"
              rel="noopener"
            >
              Report a Bug
            </a>
          </b-col>

          <b-col class="link-group">
            <strong class="section-head">Legal Stuff</strong>
            <a
              class="link"
              href="http://opensource-template.wikidot.com/legal:terms-of-use"
              target="_blank"
              rel="noopener"
            >
              Terms of Use
            </a>
            <a
              class="link"
              href="http://opensource-template.wikidot.com/legal:privacy-policy"
              target="_blank"
              rel="noopener"
            >
              Cookie Policy
            </a>
          </b-col>
          <!-- This column is used for alignment in mobile -->
          <b-col class="d-block d-sm-none"></b-col>
        </b-row>
      </b-container>
    </section>
    <section id="credits" class="text-center">
      Built by YACS under RCOS at RPI
    </section>
  </div>
</template>

<script>
import { getSemesters } from "@/services/YacsService";

export default {
  name: "Footer",
  props: {
    selectedSemester: String,
  },
  data() {
    return {
      semesterOptions: [],
    };
  },
  methods: {
    updateSelectedSemester(newSemester) {
      this.$emit("changeSelectedSemester", newSemester);
    },
  },
  computed: {
    otherSemesters() {
      return this.semesterOptions.filter(
        (semester) => semester.text != this.semester
      );
    },
  },
  created() {
    getSemesters().then((data) => {
      this.semesterOptions = data.map((s) => ({
        text: s.semester,
        value: s.semester,
      }));
    });
  },
};
</script>

<style scoped lang="scss">
#footer {
  width: 100%;
  border-top: 1px solid lightgrey;
  font-size: 15px;

  .link-group {
    @include media-breakpoint-up(sm) {
      flex-grow: 0;
      flex-basis: 0;
      color: #6c757d;
    }

    white-space: nowrap;
  }

  #main-block {
    background: white;
    color: black;
    padding-top: 25px;
    width: 100%;
    height: auto;
    margin: 0px !important;

    strong.section-head {
      color: #3d4959;
      margin-bottom: 2px;
    }

    a.link:hover {
      text-decoration: underline;
      cursor: pointer;
    }

    a.link {
      color: inherit;
      display: table;
    }

    a.link#current {
      color: grey;
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
    color: #3d4959;
  }
}
</style>
