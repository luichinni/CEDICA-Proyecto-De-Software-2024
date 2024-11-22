<template>
  <div class="box">
    <article class="media">
      <div class="media-content">
        <div class="content">
          <p>
            <strong>{{ item.titulo }}</strong>
            <br />
            <small>{{ formatDate(item.fecha) }}</small>
            <br />
            <em>{{ item.copete }}</em>
          </p>
        </div>
        <div class="has-text-right">
          <button @click="$emit('ver-detalle', item)" class="button is-link is-small">
            Leer más
          </button>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
export default {
  name: 'ListItem',
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    },
  },
};
</script>
