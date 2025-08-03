from reversi.agents.pg.agent import PGAgent
from reversi.agents.pg.trainer import Trainer
from reversi.game.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(6)
    agent = PGAgent(config, training=True)
    trainer = Trainer(agent)
    trainer.run(50000)
