<template>

  <SearchBox 
    @search="$emit('search', $event)"
  />

  <List 
    :items="items" 
    :loading="loading" 
    :error="error" 
    :nombre_elementos="nombre_elementos" 

    @ver-detalle="$emit('ver-detalle', $event)"
  />

  <div v-if="!loading && pages > 1" class="mt-5">
    <Pagination 
      :total="total" 
      :pages="pages" 
      :current_page="current_page" 
      :per_page="per_page" 

      @change-page="$emit('change-page', $event)"
    />
  </div>


</template>

<script>
import SearchBox from './SearchBox.vue';
import List from './List.vue';
import Pagination from './Pagination.vue';

export default {
  name: 'Search',
  components: {
    SearchBox,
    List,
    Pagination,
  },
  props: {
    items: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    error: {
      type: String,
      required: false,
      default: null,
    },
    nombre_elementos: {
      type: String,
      required: false,
      default: null,
    },
    total: {
      type: Number,
      required: true,
    },
    pages: {
      type: Number,
      required: true,
    },
    current_page: {
      type: Number,
      required: true,
    },
    per_page: {
      type: Number,
      required: true,
    },
  },
  emits: ['search', 'ver-detalle', 'change-page'], 
};
</script>
