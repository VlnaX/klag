# klags

Program zobrazi informaciu o offsete/lagu topiku(ov) pozadovanej konzumer skupiny.   

Pouzitie:   
klags server[:port] [group-id]
 - server - IP adresa alebo DNS meno servera s beziacim brokerom
 - port - je cislo portu, na ktorom nacuva broker (NIE Zookeeper)
 - group-id - je meno konzumer skupiny, pre ktoru chcete zobrazit informacie. Ak meno skupiny vynechate, program Vam ponukne   
   zoznam dostupnych skupin na vyber.

### Poznamka:
exe subor bol vytvoreny programom pyinstaller pod MSW 10   

   
      
      
# klags   

Display Kibana lags/offsets for requested consumer groups.   

Use:   
klags server[:port] [group-id]
 - server - is IP or DNS name of broker
 - port - is broker port (NOT Zookeeper)
 - group-id - name of consumers group. If not entered, program will display available groups to use.

### Note:   
exe file created by pyinstaller under MSW 10
