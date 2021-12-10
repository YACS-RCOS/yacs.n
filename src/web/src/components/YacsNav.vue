<script lang="ts" setup>
import { reactive, ref, watchEffect } from "vue";

const newTab = ref(null);

watchEffect(() => {
  newTab.value && newTab.value.focus();
});

const state = reactive({
  tabs: { title: "" },
  adding: false
});
</script>