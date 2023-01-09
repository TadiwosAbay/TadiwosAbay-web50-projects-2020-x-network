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
      const save_button=document.querySelectorAll('#edit');
          save_button.forEach(element=>{
                 element.onclick=function(){
                  const id=parseInt(element.dataset.id);
                  const div=document.querySelector('#posts'+id);
                  const input=document.createElement("textarea");
                  input.value=div.innerHTML;
                  const button=document.createElement("button");
                  div.innerHTML="";

                  input.name="con";
                  div.appendChild(input);
                  div.appendChild(button);
                  button.name="save";
                  button.innerHTML="save_changes";
                  div.appendChild(button);
                  button.id=parseInt("save"+id);
                  button.onclick=function(){
                    fetch(`edited/${id}/${input.value}`)
                    .then(response=>response.json())
                    .then(post=>{
                          if(post.post==="You can't edit another user's post"){
                          alert(`${post.post}`)
                        }
                        else{
                        console.log(post);
                        var x=JSON.stringify(post.post);
                        document.querySelector('#posts'+id).innerHTML=JSON.parse(x);
                      }
                    })

             }

                }
              });

});
