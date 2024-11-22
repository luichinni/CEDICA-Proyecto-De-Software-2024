<template>
  <div class="box">
    <h2 class="title is-4">Buscar</h2>

    <div class="field">
      <label class="label">Autor</label>
      <div class="control">
        <input
          type="text"
          class="input"
          placeholder="Buscar por autor"
          v-model="current_search_data.author"
        />
      </div>
    </div>

    <div class="field">
      <label class="label">Publicado desde</label>
      <div class="control">
        <input
          type="date"
          class="input"
          v-model="current_search_data.published_from"
        />
      </div>
    </div>

    <div class="field">
      <label class="label">Publicado hasta</label>
      <div class="control">
        <input
          type="date"
          class="input"
          v-model="current_search_data.published_to"
        />
      </div>
    </div>

    <div class="field">
      <div class="control">
        <button class="button is-primary is-fullwidth" @click="$emit('search', current_search_data);">
          Buscar
        </button>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "SearchBox",
  data() {
    return {
      current_search_data: {
        author: "",
        published_from: "",
        published_to: "",
      },
    };
  },
};
</script>
