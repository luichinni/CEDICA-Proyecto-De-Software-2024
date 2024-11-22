<template>
  <div v-if="loading" class="has-text-centered">
    <button class="button is-loading is-primary is-large">Cargando...</button>
  </div>

  <div v-else-if="error" class="notification is-danger has-text-centered">
    <p> {{ error }} ? {{ error }} : ⚠️ Error al cargar los {{ nombre_elementos ? nombre_elementos : 'items' }} </p>
  </div>

  <div v-if="!loading && items.length" class="mt-5">
    <ListItem 
      v-for="(item, index) in items" 
      :key="index" 
      :item="item" 
      @ver-detalle="$emit('ver-detalle', $event)"
    />
  </div>

  <p v-if="!loading && !items.length"> No hay {{ nombre_elementos ? nombre_elementos : 'items' }} disponibles. </p>

</template>

<script>
import ListItem from './ListItem.vue';

export default {
  name: 'List',
  components: {
    ListItem,
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
  },
  emits: ['ver-detalle', 'change-page'], 
};
</script>
