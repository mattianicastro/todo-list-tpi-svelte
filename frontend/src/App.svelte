<script lang="ts">

import { onMount } from 'svelte'
    import TodoContainer from './lib/TodoContainer.svelte';

  let user = null

  onMount(async () => {
    const response = await fetch(import.meta.env.VITE_API_URL + '/me', {
      credentials: 'include'
    })
    if(response.status !== 200) {
      return
    }
    user = await response.json()
  })
</script>

<div class="flex items-center justify-center min-h-screen overflow-y-scroll">
<div id="toast" class="toast toast-top toast-end z-20">
</div>
<div id="app" class="flex flex-col bg-primary rounded-lg p-5 gap-y-2 overflow-x-hidden m-2">
  <h1 class="text-2xl font-bold text-center text-primary-content">Todo List</h1>  
  {#if user}
    <TodoContainer />
  {:else}
  <a href={import.meta.env.VITE_API_URL+"/login"} class="btn btn-block">Login</a>

  {/if}

</div>
</div>
