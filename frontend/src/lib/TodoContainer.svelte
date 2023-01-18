<script lang="ts">
    import { createEventDispatcher, onMount } from 'svelte'
    import CreateTodo from './CreateTodo.svelte';
    import Todo from './Todo.svelte';


    let todos : TodoObj[] = []

    async function addTask(event) {
        const todo = event.detail as TodoObj
        todos.push(todo)
        todos = [...todos]
    }

    async function deleteTask(event) {
        const id = event.detail as number
        todos = todos.filter(todo => todo.id !== id)
    }

    async function loadTodos() {
        const response = await fetch(import.meta.env.VITE_API_URL + '/tasks', {
            credentials: 'include'
        })
        if(response.status !== 200) {
            return
        }
        todos = await response.json()
    }

    onMount(async () => {
        await loadTodos()
    })
</script>
<div class="flex flex-col gap-y-2">
<CreateTodo on:addTask={addTask}/>
{#each todos as todo}
    <Todo id={todo.id} content={todo.content} done={todo.done} on:deleteTask={deleteTask}/>
{/each}
</div>