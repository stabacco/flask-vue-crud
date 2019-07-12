
<template>
  <div>
    <code-diff :old-string="oldStr" :new-string="newStr" :outputFormat="side-by-side" />
  </div>
</template>

<script>
import vueCodeDiff from 'vue-code-diff';

export default {
  components: { CodeDiff: vueCodeDiff },
  data() {
    return {
      oldStr: 'print("stef really is the bast capit")',
      newStr: 'print("staff")',
    };
  },
};
</script>
