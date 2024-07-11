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
echo "------Database Before POST Requests------"
before=$(curl $url) 
curl $url

echo "------Generating + Sending Post Requests:------"
for i in $(seq 3)
do
    curl -X POST $url -d "$(Get_Post_Example)"
done

echo "------Database After POST Requests------"
after=$(curl $url)
curl $url

if [ "$before" = "$after" ]
then
    echo "Could not add entries!"
else
    echo "Successfully added entries!"
fi

# delete extra entries
Table_Name="timelinepost"
MySQL_Dir='C:\Program Files\MySQL\MySQL Server 8.0\bin'
. .env
cd "$MySQL_Dir"

# MAX_ID=$(./mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -e "SELECT MAX(id) FROM "$Table_Name" ")
# echo $MAX_ID
./mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -e "delete from $Table_Name where id in (SELECT id FROM (SELECT id FROM $Table_Name ORDER BY id DESC LIMIT 3) AS temp_table)"

echo "------Final Database------"
curl $url

# ./mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -e "SELECT id FROM (SELECT id FROM $Table_Name ORDER BY id DESC LIMIT 3) AS temp_table"