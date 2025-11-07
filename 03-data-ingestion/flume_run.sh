# Run Flume Agent (from Flume directory)
./bin/flume-ng agent --conf conf --conf-file conf/netcat-logger.conf --name a1 -Dflume.root.logger=INFO,console

# In another terminal
telnet localhost 44444
# Type lines; see them in the agent console
