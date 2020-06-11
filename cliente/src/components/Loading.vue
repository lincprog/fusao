<template>
  <div>
    <v-progress-circular
      :size="50"
      color="primary"
      v-show="fetching"
      :indeterminate="fetching"
    ></v-progress-circular>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['fetching'])
  }
}
</script>
