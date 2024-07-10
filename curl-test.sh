#!/bin/bash
RanNum() {
    echo $((RANDOM / 7000 + 10)) # value ranges from 0 to 32767
}


RanString(){
    var="abcdefghijklmnopqrstuvwxyz"    
    for num in $(seq $(RanNum))
    do
        name+="${var:$(( RANDOM % ${#var} )):1}"
    done

    echo $name
}


Get_Post_Example(){
    name=$(RanString)
    email="$(RanString)@$(RanString).ca"
    content=""

    for i in $(seq 4)
    do
        content+="$(RanString) "
    done
    content+="$(RanString)!"

    echo "name=$name&email=$email&content=$content"
}


url="http://127.0.0.1:5000/api/timeline_post"
curl $url 
for i in $(seq 3)
do
    curl -X POST $url -d "$(Get_Post_Example)"
done
curl $url