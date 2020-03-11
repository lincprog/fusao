<template>
  <v-card>
    <v-toolbar flat :dense="dense" :color="color" :dark="dark">
      <v-icon v-if="titleIcon">{{titleIcon}}</v-icon>
      <v-toolbar-title prepend-icon="barcode">{{title}}</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-container fluid>
        <slot/>
      </v-container>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-spacer></v-spacer>
      <slot name="acao"/>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'Panel',
  props: {
    title: String,
    color: String,
    titleIcon: String,
    dense: { type: Boolean, default: false },
    dark: { type: Boolean, default: false }
  }
}
</script>
