<script lang="ts">
    import { onMount } from 'svelte'
    import { todosStore } from '../stores';
    import CreateTodo from './CreateTodo.svelte';
    import Todo from './Todo.svelte';


    let todos : TodoObj[] = []

    todosStore.subscribe(value => todos = value)

    async function loadTodos() {
        const response = await fetch(import.meta.env.VITE_API_URL + '/tasks', {
            credentials: 'include'
        })
        if(response.status !== 200) {
            return
        }
        todosStore.set(await response.json())
    }

    onMount(async () => {
        await loadTodos()
    })
</script>
<div class="flex flex-col gap-y-2">
<CreateTodo />
{#each todos as todo}
    <Todo id={todo.id} content={todo.content} done={todo.done} />
{/each}
</div>