# find PID
omxplayer -b rtsp://192.168.1.$1:554/10
while true
   do
      PID=$(ps ax | grep omxplayer.bi[n] | cut -d ' ' -f2)
      if [$PID]
      then
         sleep 30
      else
         omxplayer -b rtsp://192.168.1.$1:554/11
         sleep 30
      fi
   done
   