<template>
  <div>{{ data.editorContent }}</div>
  <div id="ckeditor"></div>
  <el-button @click="click">获取内容</el-button>
</template>

<script>
import { onMounted, reactive } from 'vue'
//import '../../ckeditor/ckeditor5-build-classic/ckeditor'
import '../../ckeditor/ckeditor5-37.1.0-u068j2v09miw/build/ckeditor'
//import configure from '../../ckeditor/ckeditor5-37.1.0-u068j2v09miw/'
export default {
  setup() {
    var editor = null;
    const data = reactive({ 
      editor: null,
      editorContent: ""
    })

    onMounted(()=>{
      //console.log(configure);
      ClassicEditor.create(document.querySelector('#ckeditor'), {}).then(ckeditor => {
        editor = ckeditor;
      });
      // Editor.create(document.querySelector('#ckeditor'), {}).then(ckeditor => {
      //   editor = ckeditor;
      // });
      
    })

    function click() {
      var edres = editor.getData()
      data.editorContent = edres;
      console.log(edres)
      console.log(editor.ui.componentFactory.names);
    }

    return {
      data,
      click
    };
  }
}
</script>

<style>

</style>