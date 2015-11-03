# openbox-pipe-menus
Pipe menus for Openbox

## Pipe menu for Gmail  
A very simple pipe menu that shows unread count and few recent emails.  
Usage:  
Place all files in the folder gmail in ~/.config/openbox/pipemenus/gmail  
Edit ob-fetch-gmail.py to add username and password.  
Add the following line to ~/config/openbox/menu.xml  
```<menu execute="~/.config/openbox/pipemenus/gmail/ob-menu-gmail.sh" id="gmail" label="Gmail"/>```  
and the following line to ~/.config/openbox/autostart  
```while sleep 1800;do /home/macheath/.config/openbox/pipemenus/gmail/ob-fetch-gmail.py;done```  
replace 1800 by time in seconds for update interval.  
### Screen  
![screenshot](https://raw.githubusercontent.com/27himanshu/openbox-pipe-menus/master/gmail/screens/screenshot.png)
