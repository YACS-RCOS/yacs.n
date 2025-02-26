<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getProfessors, type Professor } from "@/api/professor";
import ProfessorModal from "@/components/modals/ProfessorModal.vue";

const professors = ref<Professor[]>([]);
const selectedProfessor = ref<Professor | null>(null);
const isModalOpen = ref(false);

onMounted(async () => {
  try {
    professors.value = await getProfessors();
    // professors.value.sort((a, b) => a.name.localeCompare(b.name));
    console.log(professors);
  } catch (error) {
    console.error("Error fetching professors:", error);
  }
});

function showProfessor(prof: Professor) {
  selectedProfessor.value = prof;
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
  selectedProfessor.value = null;
}
</script>

<template>
  <div class="flex flex-col text-primary gap-4 p-4">
    <h2 class="text-2xl font-bold">Professors</h2>
    <div class="flex flex-col gap-2">
      <button
        v-for="prof in professors"
        :key="prof.email"
        class="text-500 hover:underline text-left"
        @click="showProfessor(prof)"
      >
        {{ prof.name }}
      </button>
    </div>

    <ProfessorModal
      v-if="selectedProfessor"
      :prof="selectedProfessor"
      :open="isModalOpen"
      @close="closeModal"
    />
  </div>
</template>
