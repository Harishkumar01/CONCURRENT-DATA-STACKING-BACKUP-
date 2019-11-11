# CONCURRENT-DATA-STACKING-BACKUP
File Transfer is achieved by simulation of file transfer protocol using tcp socket.
The folder which has the file that is to be modified is continuously monitored using the
python library watchdog and if there is any modification in the file content it is notified
by using MQTT protocol and the backup is taken by the file transfer module.
Hence concurrent backup of the file is maintained.
