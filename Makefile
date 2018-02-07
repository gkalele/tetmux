

env/bin/activate:
	./install.sh

connect: env/bin/activate
	mkdir -p artifacts
	bash -c "source env/bin/activate;./run.py connect"

list:
	tmux list-sessions

clean:
	rm -rf env artifacts *.log

kill:
	@tmux kill-session -t c$(CLUSTER) || true
