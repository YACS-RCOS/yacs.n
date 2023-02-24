<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

    <!-- button to switch between alphabet order and category order -->
    <div style="float: left;" class="w-10">
      <b-button
        @click="listAlphabet()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >
        List by Alphabet
      </b-button>
      <br />
      <b-button
        @click="listCate()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >
        List by Department
      </b-button>

    </div>
    <CenterSpinner
      v-else
      :height="80"
      :fontSize="1.3"
      loadingMessage="Pathways"
      :topSpacing="30"
    />
  </b-container>
</template>

<script>
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  name: "Pathway",
  components: {
    CenterSpinner: CenterSpinnerComponent,
  },
  data() {
    return {
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Pathways",
        },
      ],
    };
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