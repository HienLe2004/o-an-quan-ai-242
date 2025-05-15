from game import Game
import asyncio

async def main():
    game = Game()
    # Uncomment to train RL agent before running the game 
    # await game.rl_agent.train(episodes=1000)

    await game.run()

if __name__ == "__main__":
        asyncio.run(main())