#!/bin/sh

echo "<<<homematic_addons:sep(124)>>>"
if [ -f /tmp/addon_updates.json ]; then 
  cat /tmp/addon_updates.json | grep "{"| while read i; do  echo "remote_addon|$i"; done
fi

for f in /etc/config/rc.d/*; do 
  if [ -x $f ]; then
    n=$($f info | grep Name| cut -d: -f2 ); 
    v=$($f info | grep Version| cut -d: -f 2);
    n=$(echo $n) 
    v=$(echo $v)
    echo "local_addon| { \"name\": \"$n\", \"webversion\": \"$v\" }"; 
  fi; 
done




