<script setup lang="ts">
defineProps<{ open: boolean }>();

const emit = defineEmits<{
  close: [];
}>();

defineSlots<{
  container(props: { close: () => void }): never;
  default(props: { close: () => void }): never;
}>();

const aborter = new AbortController();
let listener_active = false;

watch(
  () => props.open,
  () => {
    if (props.open && !listener_active) {
      listener_active = true;
      document.addEventListener(
        "keydown",
        (ev) => {
          if (ev.key == "Escape") {
            listener_active = false;
            aborter.abort();
            emit("close");
          }
        },
        { signal: aborter.signal }
      );
    }
  },
  { immediate: true }
);
</script>

<template>
  <div
    v-if="open"
    class="motion-safe:animate-fade-in absolute left-0 top-0 flex h-full w-full flex-col items-center justify-center bg-black bg-opacity-50"
    @click="emit('close')"
  >
    <slot
      name="container"
      :close="
        () => {
          emit('close');
        }
      "
    >
      <div
        class="my-16 flex-grow rounded bg-on-primary ring-1 ring-primary"
        @click.stop
      >
        <slot
          :close="
            () => {
              emit('close');
            }
          "
        >
          default popup content content
        </slot>
      </div>
    </slot>
  </div>
</template>
