Copyright © 2004 Cisco Systems, Inc.

Axl Sql Toolkit README File

This readme file contains information specific to the use of the AXL SQL Tool Kit.


Valid parameters for the AxlSqlToolkit command line program are:

  -username=<value>: use the specified username instead of default (CCMAdministrator)
  -password=<value>: use the specified password instead of default (ciscocisco)
  -host=<hostname or IP>: use the specified hostname
  -port=<portnumber>: use the specified portnumber (8443)
  -input=<filename>: use the specified file as the source of the sql statements (sample.xml)
  -output=<filename>: use the specified file as the destination of the AXL responses (sample.response)

In order to run the AxlSqlToolkit, you must have a recent version of the Java Runtime Environment installed.
The 1.7.0_21 or above JRE version is recommended.

From a windows system, run the following (assuming Java is in the path):

java -cp .\classes;.\lib\saaj-api.jar;.\lib\saaj-impl.jar;.\lib\mail.jar;.\lib\activation.jar;.\lib\jaxm-api.jar;.\lib\jaxm-runtime.jar;.\lib\xercesImpl.jar;.\lib\xml-apis.jar AxlSqlToolkit -username=CCMAdministrator -password=ciscocisco -host=64.101.156.207

From a linux system, run the following:

java -cp ./classes:./lib/saaj-api.jar:./lib/saaj-impl.jar:./lib/mail.jar:./lib/activation.jar:./lib/jaxm-api.jar:./lib/jaxm-runtime.jar:./lib/xercesImpl.jar:./lib/xml-apis.jar AxlSqlToolkit -username=CCMAdministrator -password=ciscocisco -host=64.101.156.207




 NOTE: There are few restrictions on the password specified by the user in "-password=<value>: use the specified password instead of default (ciscocisco)"
       -  Password cannot start with a blank. 
       -  If the password contains characters like " & ", " ^ ", " " ", " ' ", " \ ", " / ", " | ", " < ", " > " and "Space" , it has to be appropriately escaped. 
       -  If the command is run from DOS-Prompt, "space" and "&" can be escaped using double quotes while rest of all can be escaped using ^ caret. 
       -  For Example: Suppose the username=admin and password=#&12345, then the command to run the axl query from a windows machine would be:
	  java -cp .\classes;.\lib\saaj-api.jar;.\lib\saaj-impl.jar;.\lib\mail.jar;.\lib\activation.jar;.\lib\jaxm-api.jar;.\lib\jaxm-runtime.jar;.\lib\xercesImpl.jar;.\lib\xml-apis.jar AxlSqlToolkit -username=admin -password=#"&"12345 -host=64.101.156.207
	  
	  Please note & has been escaped as "&". 
