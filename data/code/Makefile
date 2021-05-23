IP = 127.0.0.1
PORT = 5000
GROUP_SIZE = 0
CONFIG = xx

run: export LHOST=$(IP)
run: export LPORT=$(PORT)
run: export MULTICAST_GROUP_SIZE=$(GROUP_SIZE)
run: export CONFIG_FILE=$(CONFIG)
run: 
	@flask run -h $(IP) -p $(PORT)

r-super: export IS_SUPERNODE=true
r-super: 
	@make run

r-node: export IS_SUPERNODE=false
r-node: 
	@make run
