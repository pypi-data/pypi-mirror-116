# idle-m
Invisible idle crypto miner

# Commands
Installation:
`pip3 install idlem -U`  

Running:
`tmux new-session -d -s "myTmuxSession" 'python3 -m idlem.run' `

Pausing:
`mp 30` - will pause for 30 minutes. Max pause is hardcoded to be 300mins

# Known issues
CentOS is not supported

# TODO:
[x] pass `hostname` as rigname for pool  
[ ] validate scheduler for all days at startup  
[ ] make sure scripts starts after restart  
[ ] check ps time for all user login shells and start mining if some shells are very old. Sometimes people just forget to detach old shells and they can stay active for weeks  
[x] allow padding users white list through CLI  
[x] make adjusting for free GPUs optional (or make it smarter and remember which GPUs were already allocated). Implemented a version which remembers. now it doesn't restart if some gpus are off due to temp limit  
