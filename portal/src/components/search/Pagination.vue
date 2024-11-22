<template>
  <nav  class="pagination is-centered mt-5" role="navigation" aria-label="pagination">
    
    <button 
      class="pagination-previous" 
      :disabled="current_page <= 1" 
      @click="$emit('change-page', current_page - 1)">
      Anterior
    </button>
    
    <button 
      class="pagination-next" 
      :disabled="current_page >= pages" 
      @click="$emit('change-page', current_page + 1)">
      Siguiente
    </button>

    <ul class="pagination-list">
      <li v-for="page in pagesArray" :key="page">
        <button 
          class="pagination-link" 
          :class="{ 'is-current': page === current_page }" 
          @click="$emit('change-page', page)">
          {{ page }}
        </button>
      </li>
    </ul>

  </nav>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
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
  computed: {
    pagesArray() {
      return Array.from({ length: this.pages }, (_, i) => i + 1);
    },
  },
};
</script>
