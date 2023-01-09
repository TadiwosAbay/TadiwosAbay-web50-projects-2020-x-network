document.addEventListener('DOMContentLoaded', function() {
      const like_button=document.querySelectorAll('#like');
      like_button.forEach(element=>{
        element.onclick=function(){
        const id=parseInt(element.dataset.id);

                fetch(`/pros/${id}`)
                .then(response=>response.json())
                .then(like=>{
                  console.log(like);
                  document.querySelector('#post'+id).innerHTML=JSON.stringify(like.like);
                })
              }
                });
              });
