<script lang="ts">
    import { getCookie } from "../utils";
    import { todosStore } from "../stores";
    let content

    async function addTodo(){
        if (!content) {
            return
        }
        const frozenContent = content
        const response = await fetch(import.meta.env.VITE_API_URL + '/tasks', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),                
            },
            body: JSON.stringify({
                content: frozenContent
            }),
            credentials: 'include'
        })
        if(response.status !== 200) {
            return
        }
        const data = await response.json()
        const todo = {
            id: data.id,
            content: frozenContent,
            done: false
        } as TodoObj
        todosStore.update(todos => [...todos, todo])
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
      <input type="text" placeholder="Insert new todo" class="input input-bordered input-ghost text-primary-content " on:keypress={handleKeyPress} bind:value={content} />
      <button class="btn flex-grow" on:click={addTodo}>+</button>
    </label>
</div>