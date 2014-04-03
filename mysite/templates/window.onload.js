<script type="text/javascript">
  window.onload = function() {
    try {
      TagCanvas.Start('myCanvas');
      TagCanvas.Start('myCanvas','weightTags', {
textFont: 'Impact,"Arial Black",sans-serif',
 textColour: '#00f' ,
 textHeight: 25,
 /* more options */
});
    } catch(e) {
      // something went wrong, hide the canvas container
      document.getElementById('myCanvasContainer').style.display = 'none';
    }
  };
</script>