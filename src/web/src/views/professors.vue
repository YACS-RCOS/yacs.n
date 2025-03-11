<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { getProfessors, type Professor } from "@/api/professor";
import ProfessorModal from "@/components/modals/ProfessorModal.vue";

const professors = ref<Professor[]>([]);
const selectedProfessor = ref<Professor | null>(null);
const isModalOpen = ref(false);
const searchTerm = ref("");

onMounted(async () => {
  try {
    professors.value = await getProfessors();
    professors.value.sort((a, b) => a.name.localeCompare(b.name));
    console.log(professors);
  } catch (error) {
    console.error("Error fetching professors:", error);
  }
});

const filteredProfessors = computed(() => {
  if (!searchTerm.value) return professors.value;
  return professors.value.filter((prof) =>
    prof.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
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

    <div class="mb-4">
      <input
        v-model="searchTerm"
        type="text"
        placeholder="Search by name"
        class="px-2 py-1 border border-gray-300 rounded text-black"
      />
    </div>

    <div class="grid grid-cols-3 gap-4">
      <button
        v-for="prof in filteredProfessors"
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
