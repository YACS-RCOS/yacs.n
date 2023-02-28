<template>
	<div class="sidebar">
		<div class="sidebar-backdrop" @click="closeSidebarPanel" v-if="isPanelOpen">
		<Transition name = "slide">
			<div v-if = "isPanelOpen"
				class = "sidebar-panel">
				<slot></slot>
			</div>
		</Transition>
		</div>
	</div>
</template>
<script>
    import { store, mutations } from '@/store.js'

    export default {
        methods: {
            closeSidebarPanel: mutations.toggleNav
        },
        computed: {
            isPanelOpen() {
                return store.isNavOpen
            }
        }
    }
</script>
<style>
	.slide-enter-active,
	.slide-enter-active
	{
		transition: transform 0.2s ease;
	}

	.slide-enter,
	.slide-leave-to{
		transform: translateX(-100%);
		translation: all 0.15s ease-in 0s;
	}

	.sidebar-backdrop {
        background-color: rgba(0,0,0,.5);
        width: 100vw;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        cursor: pointer;
    }

    .sidebar-panel {
        overflow-y: auto;
        background-color: #000000;
        position: fixed;
        left: 0;
        top: 0;
        height: 100vh;
        z-index: 999;
        padding: 3rem 20px 2rem 20px;
        width: 300px;
    }
</style>