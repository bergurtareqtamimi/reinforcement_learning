from Environment import Environment

e = Environment(10, 10) # create 10x10 grid environment

e.train(1000) # train agent 1000 times

e.test() # test agent and display path it took