<template>
  <div class="box">
    <article class="media">
      <div class="media-content">
        <div class="content">
          <p>
            <strong>{{ noticia.titulo }}</strong>
            <br />
            <small>{{ formatDate(noticia.fecha) }}</small>
            <br />
            <em>{{ noticia.copete }}</em>
          </p>
        </div>
        <!-- Enlace para ver la nota completa -->
        <div class="has-text-right">
          <button @click="$emit('ver-detalle', noticia)" class="button is-link is-small">
            Leer más
          </button>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
export default {
  name: 'NoticiaItem',
  props: {
    noticia: {
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
