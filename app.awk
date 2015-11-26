awk '{FS = "=";if ($1=="Name") printf("%s => ",$2); if($1=="Exec") {printf("%s\n",$2);nextfile;}}' /usr/share/applications/*.desktop > appnames.txt
