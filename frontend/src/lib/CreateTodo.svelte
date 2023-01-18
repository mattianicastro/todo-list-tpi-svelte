<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { getCookie } from "../utils";
    let content
	const dispatch = createEventDispatcher();

    async function addTodo(){
        const response = await fetch(import.meta.env.VITE_API_URL + '/tasks', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),                
            },
            body: JSON.stringify({
                content
            }),
            credentials: 'include'
        })
        if(response.status !== 200) {
            return
        }
        const data = await response.json()
        const todo = {
            id: data.id,
            content: content,
            done: false
        } as TodoObj
        dispatch('addTask', todo)
        content = ''
    }

    async function handleKeyPress(event: KeyboardEvent) {
        if(event.key === 'Enter') {
            await addTodo()
        }
    }
</script>
<div class="form-control">
    <label class="input-group">
      <input type="text" placeholder="Insert new todo" class="input input-bordered" on:keypress={handleKeyPress} bind:value={content} />
      <button class="btn flex-grow" on:click={addTodo}>+</button>
    </label>
</div>