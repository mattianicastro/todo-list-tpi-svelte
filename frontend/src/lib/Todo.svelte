<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { getCookie } from "../utils";

    export let content
    export let id
    export let done

    let editing = false

    const dispatch = createEventDispatcher();

    async function setTaskDone() {
        const response = await fetch(import.meta.env.VITE_API_URL + '/tasks/' + id, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),                
            },
            body: JSON.stringify({
                done: done
            }),
            credentials: 'include'
        })
        if(response.status !== 200) {
            return
        }
    }

    async function deleteTask() {
        const response = await fetch(import.meta.env.VITE_API_URL + '/tasks/' + id, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),                
            },
            credentials: 'include'
        })
        if(response.status !== 200) {
            return
        }
        dispatch('deleteTask', id)
    }

    async function updateContent(){
      const response = await fetch(import.meta.env.VITE_API_URL + '/tasks/' + id, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': getCookie('csrf_access_token'),                
                },
                body: JSON.stringify({
                    content: content
                }),
                credentials: 'include'
            })
            if(response.status !== 200) {
                return
            }
            editing = false
    }

    async function handleKeypress(event) {
      editing = true
    }
</script>


<div class="form-control">
    <div class="input-group">
      <input type="text" bind:value={content} on:change={updateContent} on:input={handleKeypress} class="flex-shrink text-primary-content input-ghost input input-bordered {editing ? 'input-warning ' : ''}" />
      <button class="btn btn-square" on:click={deleteTask}>
        <svg class="fill-secondary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M5 20a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8h2V6h-4V4a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v2H3v2h2zM9 4h6v2H9zM8 8h9v12H7V8z"/><path d="M9 10h2v8H9zm4 0h2v8h-2z"/></svg>      </button>
        <button class="btn btn-square">
            <input type="checkbox" bind:checked={done} on:change={setTaskDone} class="checkbox checkbox-lg" />
          </button>
    </div>

  </div>